#include "base.h"
#include "dlink.h"

MNM_Dlink::MNM_Dlink( TInt number_of_lane,
                      TFlt length,
                      TFlt ffs )
{
  m_ffs = ffs;
  m_number_of_lane = number_of_lane;
  m_length = length;

  m_finished_array = std::map<MNM_Dlink*, std::deque<MNM_Veh*>>();
  m_incoming_array = std::deque<MNM_Veh *>();
}

MNM_Dlink::~MNM_Dlink()
{

}

MNM_Dlink_Ctm::MNM_Dlink_Ctm( TFlt lane_hold_cap, 
                              TFlt lane_flow_cap, 
                              TInt number_of_lane,
                              TFlt length,
                              TFlt ffs,
                              TFlt unit_time,
                              TFlt flow_scalar)
  : MNM_Dlink::MNM_Dlink ( number_of_lane, length, ffs )
{
  m_lane_hold_cap = lane_hold_cap;
  m_lane_flow_cap = lane_flow_cap;
  m_flow_scalar = flow_scalar;
  m_cell_array = std::vector<Ctm_Cell*>();
  TFlt __std_cell_length = m_ffs * unit_time;
  m_num_cells = TInt(floor(m_length/__std_cell_length)); 
  if(m_num_cells == 0) {
    m_num_cells = 1;
  }
  TFlt __lane_hold_cap_last_cell = (m_length - TFlt(m_num_cells - 1) * __std_cell_length) * m_lane_hold_cap / __std_cell_length;
  TFlt __wave_speed =  m_lane_flow_cap / (m_lane_hold_cap - m_lane_flow_cap / m_ffs); //laneFlwCap/ffs is the critical density.
  m_wave_ratio = __wave_speed / m_ffs; // note that h >= 2c/v, where h is holding capacity, c is capcity, v is free flow speed. i.e., wvRatio should < 1.
  m_last_wave_ratio = (m_lane_flow_cap / (__lane_hold_cap_last_cell - m_lane_flow_cap / m_ffs))/m_ffs;
  init_cell_array(unit_time, __std_cell_length, __lane_hold_cap_last_cell);
}

int MNM_Dlink_Ctm::init_cell_array( TFlt unit_time, TFlt std_cell_length, TFlt lane_hold_cap_last_cell )
{

  Ctm_Cell *aCell = NULL;
  for(int i = 0; i<m_num_cells - 1; ++i) {
    aCell = new Ctm_Cell(TFlt(m_number_of_lane) * std_cell_length * m_lane_hold_cap, 
                         TFlt(m_number_of_lane) * m_lane_hold_cap * unit_time,
                         m_flow_scalar,
                         m_wave_ratio);
    if(aCell == NULL) {
      return 1;
    };
    m_cell_array.push_back(aCell);
    aCell = NULL;
  }
  
  //since the last cell is a non-standard cell
  if(m_length > 0.0)
    aCell = new Ctm_Cell(TFlt(m_number_of_lane) * std_cell_length * lane_hold_cap_last_cell, 
                         TFlt(m_number_of_lane) * m_lane_flow_cap * unit_time,
                         m_flow_scalar,
                         m_last_wave_ratio);
    if(aCell == NULL) {
      m_cell_array.push_back(aCell);
    }

  //compress the cellArray to reduce space 
  m_cell_array.shrink_to_fit();
  return 0;
}

int MNM_Dlink_Ctm::update_in_out_number()
{
  TFlt __temp_out_flux, __supply, __demand;
  if(m_num_cells > 1) // if only one cell, no update is needed
  {
    for (int i = 0; i < m_num_cells - 1; ++i)
    {
      __demand = m_cell_array[i]->get_demand();
      __supply = m_cell_array[i+1]->get_supply();
      __temp_out_flux = MIN(__demand, __supply) * m_flow_scalar;
      m_cell_array[i] -> m_out_veh= TInt(std::round(__temp_out_flux)); 
    }

    m_cell_array[m_num_cells - 1] -> m_out_veh = m_cell_array[m_num_cells - 1] -> m_volume;
  }
  return 0;
}

MNM_Dlink_Ctm::Ctm_Cell::Ctm_Cell(TFlt hold_cap, TFlt flow_cap, TFlt flow_scalar, TFlt wave_ratio)
{
  m_hold_cap = hold_cap;
  m_flow_cap = flow_cap;
  m_flow_scalar = flow_scalar;
  m_wave_ratio = wave_ratio;
  m_volume = TInt(0);
  m_veh_queue = std::deque<MNM_Veh*>();
}

TFlt MNM_Dlink_Ctm::Ctm_Cell::get_demand()
{
  TFlt __real_volume = TFlt(m_volume) / m_flow_scalar;
  return MIN(__real_volume, m_flow_cap);
}

TFlt MNM_Dlink_Ctm::Ctm_Cell::get_supply()
{
  TFlt __real_volume = TFlt(m_volume) / m_flow_scalar;
  if (__real_volume >= m_hold_cap) 
  {
    __real_volume = m_hold_cap;
    return TFlt(0.0);
  }
  if(m_wave_ratio <= 1.0) //this one is quite tricky, why not just __min(flwCap, hldCap - curDensity)*wvRatio? 
    return m_flow_cap > __real_volume ? m_flow_cap: TFlt((m_hold_cap - __real_volume) * m_wave_ratio);  //flowCap equals to critical density
  else 
    return MIN(m_flow_cap, TFlt(m_hold_cap - __real_volume));
}

