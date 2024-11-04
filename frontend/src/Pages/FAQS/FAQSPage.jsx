import { useEffect, useState } from 'react'
import LoadingBar from 'react-top-loading-bar'
import clients from '../../components/api/client';
import OrderProduct from './QuestionListComponent';


const FAQSPage = () => {
    const [progress, setProgress] = useState(0)
    const [orders, setOrders] = useState([]);
    const [loading, setLoading] = useState(false);
    const [NoMoredata, setNoMoredata] = useState(false);
    const [totalOrder, setTotalOrder] = useState('0');
    const [selectedStatus, setSelectedStatus] = useState('');
    const [initialOrders, setInitialOrders] = useState([]);
    useEffect(() => {
        setProgress(10);
       
          
          clients.get("api/Faqpage/")
          .then((res) => {
            setProgress(50);
            const initialOrdersData = res.data.site_identity;
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
    <>
    <div className="text-center p-4 text-2xl font-bold">FAQs</div>

{orders.map((order) => (
              <OrderProduct key={order.id} order={order} />
            ))}
    </>
  )
}

export default FAQSPage