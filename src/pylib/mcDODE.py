import os
import numpy as np
import pandas as pd
import hashlib
import time
import shutil
from scipy.sparse import coo_matrix

import MNMAPI


class MCDODE():
  def __init__(self, nb, config):
    self.config = config
    self.nb = nb
    self.num_assign_interval = nb.config.config_dict['DTA']['max_interval']
    self.ass_freq = nb.config.config_dict['DTA']['assign_frq']
    self.num_link = nb.config.config_dict['DTA']['num_of_link']
    self.num_path = nb.config.config_dict['FIXED']['num_path']
    self.num_loading_interval =  self.num_assign_interval * self.ass_freq
    self.data_dict = dict()
    self.num_data = self.config['num_data']
    self.observed_links = self.config['observed_links']
    self.paths_list = self.config['paths_list']
    self.car_count_agg_L_list = None
    self.truck_count_agg_L_list = None
    assert (len(self.paths_list) == self.num_path)

  def _add_car_link_flow_data(self, link_flow_df_list):
    assert (self.config['use_car_link_flow'])
    assert (self.num_data == len(link_flow_df_list))
    self.data_dict['car_link_flow'] = link_flow_df_list

  def _add_truck_link_flow_data(self, link_flow_df_list):
    assert (self.config['use_truck_link_flow'])
    assert (self.num_data == len(link_flow_df_list))
    self.data_dict['truck_link_flow'] = link_flow_df_list

  def _add_car_link_tt_data(self, link_spd_df_list):
    assert (self.config['use_car_link_tt'])
    assert (self.num_data == len(link_spd_df_list))
    self.data_dict['car_link_tt'] = link_spd_df_list

  def _add_truck_link_tt_data(self, link_spd_df_list):
    assert (self.config['use_truck_link_tt'])
    assert (self.num_data == len(link_spd_df_list))
    self.data_dict['truck_link_tt'] = link_spd_df_list

  def add_data(self, data_dict):
    if self.config['car_count_agg']:
      self.car_count_agg_L_list = data_dict['car_count_agg_L_list']
    if self.config['truck_count_agg']:
      self.truck_count_agg_L_list = data_dict['truck_count_agg_L_list']
    if self.config['use_car_link_flow']:
      self._add_car_link_flow_data(data_dict['car_link_flow'])
    if self.config['use_truck_link_flow']:
      self._add_truck_link_flow_data(data_dict['truck_link_flow'])
    if self.config['use_car_link_tt']:
      self._add_car_link_tt_data(data_dict['car_link_tt'])
    if self.config['use_car_link_tt']:
      self._add_truck_link_tt_data(data_dict['truck_link_tt'])

  def _run_simulation(self, f_car, f_truck):
    hash1 = hashlib.sha1()
    hash1.update(str(time.time()))
    new_folder = str(hash1.hexdigest())
    self.nb.update_demand_path2(f_car, f_truck)
    self.nb.config.config_dict['DTA']['total_interval'] = self.num_loading_interval
    self.nb.dump_to_folder(new_folder)
    a = MNMAPI.mcdta_api()
    a.initialize(new_folder)
    shutil.rmtree(new_folder)
    a.register_links(self.observed_links)
    a.register_paths(self.paths_list)
    a.install_cc()
    a.install_cc_tree()
    a.run_whole()
    return a

  def get_dar(self, dta, f_car, f_truck):
    raw_car_dar = dta.get_car_dar_matrix(np.arange(0, self.num_loading_interval, self.ass_freq), 
                np.arange(0, self.num_loading_interval, self.ass_freq) + self.ass_freq)
    # print "raw car dar", raw_car_dar
    car_dar = self._massage_raw_dar(raw_car_dar, self.ass_freq, f_car, self.num_assign_interval)
    raw_truck_dar = dta.get_truck_dar_matrix(np.arange(0, self.num_loading_interval, self.ass_freq), 
                np.arange(0, self.num_loading_interval, self.ass_freq) + self.ass_freq)
    truck_dar = self._massage_raw_dar(raw_truck_dar, self.ass_freq, f_truck, self.num_assign_interval)
    # print "dar", car_dar, truck_dar
    return (car_dar, truck_dar)

  def _massage_raw_dar(self, raw_dar, ass_freq, f, num_assign_interval):
    num_e_path = len(self.paths_list)
    num_e_link = len(self.observed_links)
    small_assign_freq = ass_freq * self.nb.config.config_dict['DTA']['unit_time'] / 60
    link_seq = (np.array(map(lambda x: self.observed_links.index(x), raw_dar[:, 2].astype(np.int)))
                + raw_dar[:, 3] * num_e_link / ass_freq).astype((np.int))
    path_seq = (raw_dar[:, 0] + (raw_dar[:, 1] / small_assign_freq).astype(np.int) * num_e_path).astype(np.int)
    # print path_seq
    p = raw_dar[:, 4] / f[path_seq]

    mat = coo_matrix((p, (link_seq, path_seq)), 
                   shape=(num_assign_interval * num_e_link, num_assign_interval * num_e_path))
    return mat    

  def init_path_flow(self, car_scale = 1, truck_scale = 0.1):
    f_car =  np.random.rand(self.num_assign_interval * self.num_path) * car_scale
    f_truck =  np.random.rand(self.num_assign_interval * self.num_path) * truck_scale
    return (f_car, f_truck)

  def compute_path_flow_grad_and_loss(self, one_data_dict, f_car, f_truck):
    print "Running simulation"
    dta = self._run_simulation(f_car, f_truck)
    print "Getting DAR"
    (car_dar, truck_dar) = self.get_dar(dta, f_car, f_truck)
    print "Evaluating grad"
    car_grad = np.zeros(len(self.observed_links) * self.num_assign_interval)
    truck_grad = np.zeros(len(self.observed_links) * self.num_assign_interval)
    if self.config['use_car_link_flow']:
      print "car link flow"
      car_grad += self.config['link_car_flow_weight'] * self._compute_grad_on_car_link_flow(dta, one_data_dict)
    if self.config['use_truck_link_flow']:
      truck_grad += self.config['link_truck_flow_weight'] * self._compute_grad_on_truck_link_flow(dta, one_data_dict)
    # if self.config['use_link_tt']:
    #   grad += self.config['link_tt_weight'] * self._compute_grad_on_link_tt(dta, one_data_dict['link_tt'])
    print "Getting Loss"
    loss = self._get_loss(one_data_dict, dta)
    return  car_dar.T.dot(car_grad), truck_dar.T.dot(truck_grad), loss

  def _compute_grad_on_car_link_flow(self, dta, one_data_dict):
    link_flow_array = one_data_dict['car_link_flow']
    x_e = dta.get_link_car_inflow(np.arange(0, self.num_loading_interval, self.ass_freq), 
                  np.arange(0, self.num_loading_interval, self.ass_freq) + self.ass_freq).flatten(order = 'F')
    # print "x_e", x_e, link_flow_array
    if self.config['car_count_agg']:
        x_e = one_data_dict['car_count_agg_L'].dot(x_e)
    grad = -np.nan_to_num(link_flow_array - x_e)
    if self.config['car_count_agg']:
      grad = one_data_dict['car_count_agg_L'].T.dot(grad)
    # print "final link grad", grad
    return grad
  
  def _compute_grad_on_truck_link_flow(self, dta, one_data_dict):
    link_flow_array = one_data_dict['truck_link_flow']
    x_e = dta.get_link_truck_inflow(np.arange(0, self.num_loading_interval, self.ass_freq), 
                  np.arange(0, self.num_loading_interval, self.ass_freq) + self.ass_freq).flatten(order = 'F')
    if self.config['truck_count_agg']:
        x_e = one_data_dict['truck_count_agg_L'].dot(x_e)
    grad = -np.nan_to_num(link_flow_array - x_e)
    if self.config['truck_count_agg']:
      grad = one_data_dict['truck_count_agg_L'].T.dot(grad)
    return grad

  # def _compute_grad_on_link_tt(self, dta, link_flow_array):
  #   tt_e = dta.get_link_tt(np.arange(0, self.num_loading_interval, self.ass_freq))
  #   tt_free = list(map(lambda x: self.nb.get_link(x).get_fft(), self.observed_links))
  #   for i in range(tt_e.shape[0]):
  #     pass


  def _get_one_data(self, j):
    assert (self.num_data > j)
    one_data_dict = dict()
    if self.config['use_car_link_flow']:
      one_data_dict['car_link_flow'] = self.data_dict['car_link_flow'][j]
    if self.config['use_truck_link_flow']:
      one_data_dict['truck_link_flow'] = self.data_dict['truck_link_flow'][j]
    if self.config['use_car_link_tt']:
      one_data_dict['car_link_tt'] = self.data_dict['car_link_tt'][j]
    if self.config['use_truck_link_tt']:
      one_data_dict['truck_link_tt'] = self.data_dict['truck_link_tt'][j]
    if self.config['car_count_agg']:
      one_data_dict['car_count_agg_L'] = self.car_count_agg_L_list[j]
    if self.config['truck_count_agg']:
      one_data_dict['truck_count_agg_L'] = self.truck_count_agg_L_list[j]
    return one_data_dict


  def _get_loss(self, one_data_dict, dta):
    loss = np.float(0)
    if self.config['use_car_link_flow']:
      x_e = dta.get_link_car_inflow(np.arange(0, self.num_loading_interval, self.ass_freq), 
                  np.arange(0, self.num_loading_interval, self.ass_freq) + self.ass_freq).flatten(order = 'F')
      if self.config['car_count_agg']:
        x_e = one_data_dict['car_count_agg_L'].dot(x_e)
      loss += self.config['link_car_flow_weight'] * np.linalg.norm(np.nan_to_num(x_e - one_data_dict['car_link_flow']))
    if self.config['use_truck_link_flow']:
      x_e = dta.get_link_truck_inflow(np.arange(0, self.num_loading_interval, self.ass_freq), 
                  np.arange(0, self.num_loading_interval, self.ass_freq) + self.ass_freq).flatten(order = 'F')
      if self.config['truck_count_agg']:
        x_e = one_data_dict['truck_count_agg_L'].dot(x_e)
      loss += self.config['link_truck_flow_weight'] * np.linalg.norm(np.nan_to_num(x_e - one_data_dict['truck_link_flow']))
    return loss



  def estimate_path_flow(self, step_size = 0.1, max_epoch = 10, car_init_scale = 10, truck_init_scale = 1):
    (f_car, f_truck) = self.init_path_flow(car_scale = car_init_scale, truck_scale = truck_init_scale)
    for i in range(max_epoch):
      seq = np.random.permutation(self.num_data)
      loss = np.float(0)
      for j in seq:
        one_data_dict = self._get_one_data(j)
        car_grad, truck_grad, tmp_loss = self.compute_path_flow_grad_and_loss(one_data_dict, f_car, f_truck)
        # print "gradient", car_grad, truck_grad
        f_car -= car_grad * step_size / np.sqrt(i+1)
        f_truck -= truck_grad * step_size / np.sqrt(i+1)
        loss += tmp_loss
      print "Epoch:", i, "Loss:", loss / np.float(self.num_data)
      # print f_car, f_truck
      # break
    return (f_car, f_truck)


  def generate_route_choice(self):
    pass