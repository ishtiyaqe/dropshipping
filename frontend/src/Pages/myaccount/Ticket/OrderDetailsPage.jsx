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
  const [smsData, setSmsData] = useState([]);
  const [userId, setUserId] = useState(0);
  const [process, setprocess] = useState('');
  const smsContainerRef = useRef();
  const [message, setMessage] = useState('');
  const [sendMessage, setSendMessage] = useState('');
  const [isPopupVisible, setIsPopupVisible] = useState(false); // State to manage popup visibility
  const [progress, setProgress] = useState(0)
  
  
  
  
  
  
  useEffect(() => {
    setProgress(10);

    clients
      .get(`/TicketSms/${order.data.ticket_no}`)
      .then(function (res) {
        setProgress(50);
        const initialOrders = Object.values(res.data.sms);
        setSmsData(initialOrders);
        
        setUserId(res.data.user)

        if (smsContainerRef.current) {
          smsContainerRef.current.scrollTop = smsContainerRef.current.scrollHeight;
        }
        setProgress(100);
      })
      .catch(function (error) {
        setProgress(50);
        setSmsData([]);
        setProgress(100);
      });
  }, [setSmsData]);



  const fetchSmsData = () => {
    clients
      .get(`/TicketSms/${order.data.ticket_no}`)
      .then(function (res) {
        const initialOrders = Object.values(res.data.sms);
        setSmsData(initialOrders);
        
        setUserId(res.data.user);
        
       
      })
      .catch(function (error) {
        setSmsData([]);
      });
  };

  // useEffect with cleanup to avoid memory leaks
  useEffect(() => {
    // Fetch initial data
    fetchSmsData();

    // Set up interval to fetch data every 3 seconds
    const intervalId = setInterval(() => {
      fetchSmsData();
    }, 2000);

    // Clean up the interval when the component unmounts
    return () => clearInterval(intervalId);
  }, []); // The empty dependency array ensures that this effect runs only once when the component mounts




  // Function to toggle the timeline visibility
  const toggleTimeline = () => {
    setShowTimeline(!showTimeline);
    setprocess(order)
  };
  const onClosesclass = () => {
    order.onClose(true)
  }


  const handleChange = (e) => {
    setMessage(e.target.value);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await clients.post(`/TicketSms/${order.data.ticket_no}`, { messae: message });
      setSendMessage(response.data); // You can handle the new message data as needed
      setMessage(''); // Clear the message input after successful submission
      setTimeout(() => {
        fetchSmsData();
    
        if (smsContainerRef.current) {
          smsContainerRef.current.scrollTop = smsContainerRef.current.scrollHeight;
        }
      }, 2000); // 3000 milliseconds = 3 seconds
      // Check if smsContainerRef is available
  
    } catch (error) {
      console.error('Error sending message:', error);
    }
  };
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
          <p className="text-sm font-bold  self-center ">Order Id: {order.data.ticket_no}
            <span className="text-xs font-normal "> Order date: <TimeComponent timestamp={order.data.created_at} /></span>
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
                Ticket Messsage:
                <div className="p-2">

                  <p className="mt-1 text-sm text-gray400 "><b >Message: {order.data.message}</b></p>
                  <p className="mt-1 text-sm text-gray400 "><b >Subject: {order.data.subject}</b></p>
                  <p className="mt-1 text-sm text-gray400 "><b >Status: {order.data.status}</b></p>
                </div>


              </div>
            </div>
          </div>




        </div>

        <div className="">
          <div className="mb-4 space-y-2 flex flex-col justify-center">


            <div className="  border border-gray-400 rounded w-1/1 overflow-y-auto"
             style={{ height: '250px', direction: 'rtl', overflowX: 'hidden' }}
        ref={smsContainerRef}>
{!smsData || smsData.length === 0 ? (
  <div className='text-center'>No Message</div>
) : (
  smsData.map((sms, index) => (
    <div key={index} className={`col-start-${sms.user === userId ? 6 : 1} ${sms.user === userId ? 'user-sms' : 'admin-sms'} col-end-${sms.user === userId ? 13 : 8} p-3 rounded-lg`}>
      <div className="flex flex-col justify-start">
        <div className={`relative ${sms.user === userId ? 'mr-3 bg-indigo-100' : 'ml-3 bg-lime-600 text-white'} text-sm py-2 px-4 shadow rounded-xl`}>
          <div>{sms.messae}</div>
        </div>
        <div className='text-xs mt-1 text-gray-400'>
          <TimeComponent timestamp={sms.created_at} />
        </div>
      </div>
    </div>
  ))
)}







            </div>
            <div className="  bottom-0 w-full">
              <form onSubmit={handleSubmit}>
              <div
                class="flex flex-row items-center h-16 rounded-xl bg-white w-full px-4"
              >

                <div class="flex-grow ">
                  <div class="relative w-full">
                    <input
                      type="text"
                      value={message} 
                      onChange={handleChange}
                      class="flex w-full border rounded-xl focus:outline-none focus:border-indigo-300 pl-4 h-10 bg-white"
                    />

                  </div>
                </div>
                  <button
                  type="submit"
                    class="flex items-center justify-center theme_color theme_colorl rounded-xl text-white px-4 py-1 flex-shrink-0"
                  >
                    <span>Send</span>
                    <span class="ml-2">
                      <svg
                        class="w-4 h-4 transform rotate-45 -mt-px"
                        fill="none"
                        stroke="currentColor"
                        viewBox="0 0 24 24"
                        xmlns="http://www.w3.org/2000/svg"
                      >
                        <path
                          stroke-linecap="round"
                          stroke-linejoin="round"
                          stroke-width="2"
                          d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"
                        ></path>
                      </svg>
                    </span>
                  </button>
               


              
              </div>
                 </form>
            </div>

          </div>
        </div>


        <hr className='mt-2 mb-2' />

        <div className="p-2 flex justify-center">
          <p className="text-sm "><b>&nbsp;&nbsp;Last Updated AT: &nbsp;</b><TimeComponent timestamp={order.data.updated_at} /></p>
        </div>

      </div>
      {/* </div> */}
    </>
  )
}

export default OrderDetailsPage