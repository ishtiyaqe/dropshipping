import React, { useEffect, useState } from 'react';
import clients from '../../../components/api/Client';
import OrderProduct from './OrderProductComponent';
import FilterAltTwoToneIcon from '@mui/icons-material/FilterAltTwoTone';
import LoadingBar from 'react-top-loading-bar'

const OrderPage = () => {
  const [progress, setProgress] = useState(0)
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(false);
  const [NoMoredata, setNoMoredata] = useState(false);
  const [totalOrder, setTotalOrder] = useState('0');
  const [selectedStatus, setSelectedStatus] = useState('');
  const [initialOrders, setInitialOrders] = useState([]);
  
  const loadMoreOrders = () => {
    setProgress(10);
    setLoading(true);
    if (totalOrder === orders.length) {
      setNoMoredata(true);
    } else {
      clients.get(`/order-more-data?limit=10&offset=${orders.length}`)
      .then((response) => {
          setProgress(50);
          setOrders([...orders, ...response.data.orders_p]);
          setLoading(false);
          setProgress(100);
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
    clients.get("/api/total-order-products/")
      .then((res) => {
        setProgress(50);
        const totalAmount = res.data.total_orders;
        setTotalOrder(totalAmount);
        setProgress(100);
      })
      .catch(() => {
        setProgress(60);
        setTotalOrder('0');
        setProgress(100);
      });
      
      clients.get("api/all-order-products/")
      .then((res) => {
        setProgress(50);
        const initialOrdersData = res.data.total_orders;
        setOrders(initialOrdersData);
        setInitialOrders(initialOrdersData);
        setProgress(100);
      })
      .catch(() => {
        setProgress(50);
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

      <div className="w-full grid grid-cols-1 gap-4">
        <div className="dark:shadow-gray-400 flex justify-between mb-4 shadow-md rounded-lg p-4 text-white text-xl font-semibold bg-gradient-to-r from-orange-600 to-orange-400">
          Orders: ({totalOrder})
          <button onClick={() => setSliderVisible(!sliderVisible)}>
            <FilterAltTwoToneIcon></FilterAltTwoToneIcon>
          </button>
        </div>
      </div>

      <div className={`bg-white w-full ${sliderVisible ? 'duration-300' : 'hidden'}`}>
        <label className='absolute right-0 mr-10 '>
          <select
            className='bg-white text-black p-2 w-full rounded-md shadow-md dark:shadow-gray-200 border'
            value={selectedStatus}
            onChange={(e) => {
              setSelectedStatus(e.target.value);
              filterOrders(e.target.value);
            }}
          >
            <option style={{ color: 'black' }} value="all">All</option>
            <option style={{ color: 'black' }} value="Order Placed">Order Placed</option>
            {/* Add other options as needed */}
          </select>
        </label>
      </div>

      <div className=" mb-4 ">
        {orders.length === 0 ? (
          <div>
            <br />
            <p className="flex justify-center">No Order Found!!</p>
            <br />
          </div>
        ) : (
          <div id="filteredProducts" className='flex flex-col space-y-4'>
            {orders.map((order) => (
              <OrderProduct key={order.OrderP_id} order={order} />
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
            className={`self-center ticket theme_color theme_colorl text-white rounded-lg shadow-lg p-2 ${NoMoredata ? 'hidden' : ''}`}
            onClick={loadMoreOrders}
          >
            Load More {loading && <i className="fa fa-sync load-more-icon px-2"></i>}
          </button>
        </p>
      )}

    </div>
  );
};

export default OrderPage;
