import React, { useState, useEffect, useRef } from 'react';
import { Link } from 'react-router-dom';
import ProgressBarComponent from './ProgressBarComponent'
import TimeComponent from '../../../components/FrontendTheme/timeClearComponenet'
import OrderDetailsPopup from './OrderDetailsPopup';
import clients from '../../../components/api/Client';
import CloseIcon from '@mui/icons-material/Close';
import LoadingBar from 'react-top-loading-bar'

const OrderDetailsPage = (order) => {
  const [showTimeline, setShowTimeline] = useState(false);
  const [progress, setProgress] = useState(0)




  const onClosesclass = () => {
    order.onClose(true)
  }



  return (

    <>
      <LoadingBar
        color='#f11946'
        progress={progress}
        onLoaderFinished={() => setProgress(0)}
      />
      {/* <div className="fixed inset-0 z-50 flex items-center justify-center backdrop-blur-sm "> */}
      <div className="border p-4 product-box rounded-md shadow-md  ">
        <div className='flex justify-between'>
          <p className="text-sm font-bold  self-center ">Status: {order.data.status}
            <span className="text-xs font-normal "> Submited date: <TimeComponent timestamp={order.data.created_at} /></span>
          </p>

          <button
            className="self-center font-bold drop-shadow-md text-rose-500 p-1"
            onClick={onClosesclass}
          >

            <CloseIcon />
          </button>
        </div>
        <hr className="p-1" />


        <div className="flex   flex-col">
          <div className="w-full">
            <div className="flex lg:flex-row flex-col leading-5">

              <div className="lg:ml-3 ml-0 mb-4">
                {order.data.orderi}
                <br />
                Amount Details Messsage:
                <div className="p-2">

                  <p className="mt-1 text-sm text-gray400 "><b >Wallet Amount: {order.data.amount}</b></p>
                  <p className="mt-1 text-sm text-gray400 "><b >Transaction Method: {order.data.t_m}</b></p>
                  <p className="mt-1 text-sm text-gray400 "><b >Transaction Id: {order.data.t_id}</b></p>
                  <p className="mt-1 text-sm text-gray400 "><b >Note: {order.data.note}</b></p>
                  <p className="mt-1 text-sm text-gray400 "><b >Status: {order.data.status}</b></p>
                </div>


              </div>
            </div>
          </div>




        </div>











      </div>


      <hr className='mt-2 mb-2' />

      <div className="p-2 flex justify-center">
        <p className="text-sm "><b>&nbsp;&nbsp;Last Updated AT: &nbsp;</b><TimeComponent timestamp={order.data.updated_at} /></p>
      </div>


      {/* </div> */}
    </>
  )
}

export default OrderDetailsPage