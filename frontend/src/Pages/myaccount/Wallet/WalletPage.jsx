import React,{useState, useEffect} from 'react'
import LoadingBar from 'react-top-loading-bar'
import clients from '../../../components/api/Client';
import OrderProduct from './OrderProductComponent';
import FilterAltTwoToneIcon from '@mui/icons-material/FilterAltTwoTone';
import OrderDetailsPopup from './OrderDetailsPopup'

const TicketPage = () => {
  const [progress, setProgress] = useState(0)
  const [isPopupVisible, setIsPopupVisible] = useState(false); // State to manage popup visibility
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(false);
  const [NoMoredata, setNoMoredata] = useState(false);
  const [totalOrder, setTotalOrder] = useState('0');
  const [selectedStatus, setSelectedStatus] = useState('');
  const [initialOrders, setInitialOrders] = useState([]);
  const [isAdmin, setIsAdmin] = useState(false);






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
      .get('/wallet/balance/')
      .then(function (res) {
        setProgress(50);
        const initialOrders = Object.values(res.data.History);
        setOrders(initialOrders);
        
  
        setInitialOrders(initialOrders);
        setTotalOrder(res.data.wallet_balance);
     
        setProgress(100);
      })
      .catch(function (error) {
        setProgress(50);
        setTotalOrder('0');
        setOrders([]);
        setProgress(100);
      });
  }, [setOrders]);
  const handleChange = () => {
    setIsPopupVisible(true);
  };
  return (
    <div>
       <LoadingBar
        color='#f11946'
        progress={progress}
        onLoaderFinished={() => setProgress(0)}
      />
      {loading && <p>Loading...</p>}

      <div className=" ">
        <div className="dark:shadow-gray-400 flex justify-between mb-4 shadow-md rounded-lg p-2 text-white text-xl font-semibold bg-gradient-to-r from-orange-600 to-orange-400">
        Wallet: (৳ {totalOrder}) 
          <button onClick={() => setSliderVisible(!sliderVisible)}>
            <FilterAltTwoToneIcon></FilterAltTwoToneIcon>
          </button>

        </div>
      </div>
          <div onClick={handleChange} className='cursor-pointer theme_color theme_colorl p-4 flex justify-end w-fit text-white ml-auto rounded-md shadow-md'>
            Add New Fund
            </div>
            {isPopupVisible && (
          <>

            <OrderDetailsPopup  onClose={() => setIsPopupVisible(false)} />

          </>

        )}
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
            <option value="Approved">Approved</option>
            <option value="Pending">Pending</option>
            <option value="Cancel">Cancel</option>
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
              <OrderProduct key={order.id} order={order} />
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
            className={`self-center ticket bg-blue-600 text-white rounded-lg shadow-lg p-2 ${
              NoMoredata ? 'hidden' : ''
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

export default TicketPage