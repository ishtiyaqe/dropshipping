import { useEffect, useState } from 'react'
import LoadingBar from 'react-top-loading-bar'
import clients from '../../components/api/client';


const AboutPage = () => {
    const [progress, setProgress] = useState(0)
    const [orders, setOrders] = useState([]);
    const [loading, setLoading] = useState(false);
    const [NoMoredata, setNoMoredata] = useState(false);
    const [totalOrder, setTotalOrder] = useState('0');
    const [selectedStatus, setSelectedStatus] = useState('');
    const [initialOrders, setInitialOrders] = useState([]);
    useEffect(() => {
        setProgress(10);
       
          
          clients.get("api/aboustuspageList/")
          .then((res) => {
            setProgress(50);
            const initialOrdersData = res.data.Abou_us;
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
    <div className="text-center p-4 text-2xl font-bold">About us</div>

{orders.map((order) => (
              // <OrderProduct key={order.id} order={order} />
              <div key={order.id} dangerouslySetInnerHTML={{ __html: order.aboutus }} />
            ))}
    </>
  )
}

export default AboutPage