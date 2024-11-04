import React, { useState, useEffect } from 'react';
import "react-step-progress-bar/styles.css";
import { ProgressBar, Step } from 'react-step-progress-bar';
import { PendingActionsTwoTone as PendingActionsTwoToneIcon } from '@mui/icons-material';
import TaskAltTwoToneIcon from '@mui/icons-material/TaskAltTwoTone';
import PlaylistAddCheckTwoToneIcon from '@mui/icons-material/PlaylistAddCheckTwoTone';
import Inventory2TwoToneIcon from '@mui/icons-material/Inventory2TwoTone';
import LocalShippingTwoToneIcon from '@mui/icons-material/LocalShippingTwoTone';
import FlightTakeoffIcon from '@mui/icons-material/FlightTakeoff';
import WarehouseIcon from '@mui/icons-material/Warehouse';
import HomeIcon from '@mui/icons-material/Home';

const RqoProcesBard = () => {
  const [activeSteps, setActiveSteps] = useState([]);
  const totalSteps = 6;
  useEffect(()=>{
    setActiveSteps([0, 1, 2, 3,4,5])
  })
  const ProgressStep = ({ iconComponent, text }) => {
    return (
      <div className='flex  flex-col justify-center text-center theme_color rounded-full w-20 h-20 overflow-clip  text-white'>
        {iconComponent ? (
          <div className='self-center text-xs'>
            {iconComponent}
          </div>
        ) : (
          <i className="material-icons">check</i>
        )}
        <p className='text-xs'>{text}</p>
      </div>
    );
  }
  return (
   <>
 
 
            <ProgressStep iconComponent={<PendingActionsTwoToneIcon  />} text="Create List" />
        
        
        
            <ProgressStep iconComponent={<PlaylistAddCheckTwoToneIcon />} text="Take Rate" />
         
            <ProgressStep iconComponent={<Inventory2TwoToneIcon />} text="Received in Warehouse" />
         
            <ProgressStep iconComponent={<FlightTakeoffIcon />} text="Shipped to BD" />
       
            <ProgressStep iconComponent={<WarehouseIcon />} text="Received in BD" />
        
            <ProgressStep iconComponent={<HomeIcon />} text="Deliver to Doorstep" />
          
   </>
  )
}

export default RqoProcesBard