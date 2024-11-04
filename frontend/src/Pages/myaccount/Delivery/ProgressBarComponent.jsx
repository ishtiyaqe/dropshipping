import React, { useState, useEffect } from 'react';
import "react-step-progress-bar/styles.css";
import { ProgressBar, Step  } from 'react-step-progress-bar';
import { PendingActionsTwoTone as PendingActionsTwoToneIcon } from '@mui/icons-material';
import TaskAltTwoToneIcon from '@mui/icons-material/TaskAltTwoTone';
import PlaylistAddCheckTwoToneIcon from '@mui/icons-material/PlaylistAddCheckTwoTone';
import Inventory2TwoToneIcon from '@mui/icons-material/Inventory2TwoTone';
import LocalShippingTwoToneIcon from '@mui/icons-material/LocalShippingTwoTone';

function ProgressBarComponet({ process }) {
  const [activeSteps, setActiveSteps] = useState([]);
const totalSteps = 4
  useEffect(() => {
    // Define your logic to set active steps based on the 'process' variable
    switch (process) {
      case "Order pending":
      case "Order Refund Request":
      case "Order Refunded":
      case "Refund Closed":
        setActiveSteps([0]);
        break;
      case "Order processing":
      case "Order Shipped":
        setActiveSteps([0, 1]);
        break;
      case "Order Received":
      case "Partial Payment Pending":
      case "Partial Payment Received":
      case "Delivery Request":
        setActiveSteps([0, 1, 2]);
        break;
      case "Order Delivered":
      case "Delivered":
        setActiveSteps([0, 1, 2, 3]);
        break;
      default:
        setActiveSteps([0]);
        break;
    }
  }, [process]);

  return (
    <div >
    <ProgressBar
    percent={(activeSteps.length / totalSteps) * 100}
      filledBackground="linear-gradient(to right, #fefb72, #f0bb31)"
    >
      <Step transition="scale">
          {({ accomplished }) => (
         
      <ProgressStep iconComponent={<PendingActionsTwoToneIcon cl />} text="pending" />
          )}
        </Step>
      <Step transition="scale">
          {({ accomplished }) => (
         
      <ProgressStep iconComponent={<PlaylistAddCheckTwoToneIcon />} text="Processing" />
          )}
        </Step>
      <Step transition="scale">
          {({ accomplished }) => (
         
      <ProgressStep iconComponent={<Inventory2TwoToneIcon />} text="Received" />
          )}
        </Step>
      <Step transition="scale">
          {({ accomplished }) => (
         
      <ProgressStep iconComponent={<LocalShippingTwoToneIcon />} text="Delivered" />
          )}
        </Step>
    </ProgressBar>
    </div>
  );
}

function ProgressStep({ iconComponent, text }) {
  return (
    <div className='flex flex-col justify-center text-center'>
      {iconComponent ? (
        <div>
          {iconComponent}
        </div>
      ) : (
        <i className="material-icons">check</i>
      )}
      <p className='text-xs'>{text}</p>
    </div>
  );
}

export default ProgressBarComponet;
