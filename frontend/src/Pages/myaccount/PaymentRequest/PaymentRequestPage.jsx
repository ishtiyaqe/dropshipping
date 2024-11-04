import React, { useEffect, useState } from 'react';
import clients from '../../../components/api/Client';
import OrderProduct from './OrderProductComponent';
import FilterAltTwoToneIcon from '@mui/icons-material/FilterAltTwoTone';
import LoadingBar from 'react-top-loading-bar'

const PaymentRequestPage = () => {
  const [progress, setProgress] = useState(0)
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(false);
  const [NoMoredata, setNoMoredata] = useState(false);
  const [totalOrder, setTotalOrder] = useState('0');
  const [selectedStatus, setSelectedStatus] = useState('');
  const [initialOrders, setInitialOrders] = useState([]);

  
  
  
  
  

  const loadMoreOrders = () => {
    setLoading(true);
    if (totalOrder === orders.length) {
      setNoMoredata(true);
    } else {
      clients.get(`/order-more-data?limit=10&offset=${orders.length}`).then((response) => {
        
        setOrders([...orders, ...response.data.orders_p]);
        setLoading(false);
      });
    }
  };

  const [sliderVisible, setSliderVisible] = useState(false);

  const filterOrders = (status) => {
    if (status === 'all') {
      setOrders(initialOrders);
    } else {
      const filteredOrders = initialOrders.filter((order) => order.status === status);
      setOrders(filteredOrders);
    }
  };

  useEffect(() => {
    setProgress(10);
    clients
      .get('api/PaymentOrder/')
      .then(function (res) {
        setProgress(50);
        const initialOrders = res.data.paymentorder;
        setOrders(initialOrders);
        
        setInitialOrders(initialOrders);
        setTotalOrder(res.data.total_orders);
        setProgress(100);
      })
      .catch(function (error) {
        setProgress(50);
        setTotalOrder('0');
        setOrders([]);
        setProgress(100);
      });
  }, []);

  return (
    <div>
      <LoadingBar
        color='#f11946'
        progress={progress}
        onLoaderFinished={() => setProgress(0)}
      />
      {loading && <p>Loading...</p>}

      <div className=" ">
        <div className="dark:shadow-gray-400 flex justify-between mb-4 shadow-md rounded-lg p-4 text-white text-xl font-semibold bg-gradient-to-r from-orange-600 to-orange-400">
          Payment Request: ({totalOrder})
          <button onClick={() => setSliderVisible(!sliderVisible)}>
            <FilterAltTwoToneIcon></FilterAltTwoToneIcon>
          </button>
        </div>
      </div>
      <div className={`bg-white w-full ${sliderVisible ? 'duration-300' : 'hidden'}`}>
        <label className="absolute right-0 mr-10 ">
          <select
            className="bg-white text-black p-2 w-full rounded-md shadow-md dark:shadow-gray-200 border"
            value={selectedStatus}
            onChange={(e) => {
              setSelectedStatus(e.target.value);
              filterOrders(e.target.value);
            }}
          >
            <option value="all">All</option>
            <option value="Payment Pending">Payment Pending</option>
<option value="Payment Confirm">Payment Confirm</option>
<option value="Payment Confirm Pending">Payment Confirm Pending</option>
<option value="Payment SucessFull">Payment SucessFull</option>
<option value="Payment Closed">Payment Closed</option>


          </select>
        </label>
      </div>

      <div className="dark:shadow-gray-400 mb-4 shadow-lg rounded-lg p-4">
        {orders.length === 0 ? (
          <div>
            <br />
            <p className="flex justify-center">No Order Found!!</p>
            <br />
          </div>
        ) : (
          <div id="filteredProducts" className="flex flex-col space-y-4">
            {orders.map((order) => (
              <OrderProduct key={order.payment_id} order={order} />
            ))}
          </div>
        )}
      </div>

      {!NoMoredata && (
        <p className="my-4 text-center">
          <button
            id="loadMore"
            data-total={totalOrder}
            data-limit="10"
            className={`self-center ticket bg-blue-600 text-white rounded-lg shadow-lg p-2 ${NoMoredata ? 'hidden' : ''
              }`}
            onClick={loadMoreOrders}
          >
            Load More {loading && <i className="fa fa-sync load-more-icon px-2"></i>}
          </button>
        </p>
      )}
    </div>
  );
};

export default PaymentRequestPage;
