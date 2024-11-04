


import { Route, createBrowserRouter, createRoutesFromElements, RouterProvider } from 'react-router-dom';
import Home from './Pages/home/HomePage';
import Login from './Pages/auth/Login';
import Register from './Pages/auth/Register';
import Header from './components/nav/Header';
import CartPage from './Pages/cart/CartPage';
import AboutPage from './Pages/Abouutus/AboutPage';
import ProductDetails from './Pages/products/ProductDetailsPage';
import CheckOutPage from './Pages/checkout/CheckOutPage';
import MyAccountPage from './Pages/myaccount/MyAccountPage';
import Dashboard from './Pages/myaccount/dashboard/Dashboard';
import OrderPage from './Pages/myaccount/order/OrderPage';
import RequestOrdersPage from './Pages/myaccount/RequestOrders/RequestOrdersPage';
import PaymentRequestPage from './Pages/myaccount/PaymentRequest/PaymentRequestPage';
import ShippingRequestPage from './Pages/myaccount/ShippingRequest/ShippingRequestPage';
import DeliveryPage from './Pages/myaccount/Delivery/DeliveryPage';
import TicketPage from './Pages/myaccount/Ticket/TicketPage';
import Wallet from './Pages/myaccount/Wallet/WalletPage';
import SearchPage from './Pages/search/SearchPage';
import StorePage from './Pages/shop/ShopPage';
import ReqOrderFormPage from './Pages/ReqOrder/ReqOrderFormPage';
import PayForMePage from './Pages/PayForMe/PayForMePage';
import ShipForMePage from './Pages/ShipForme/ShipForMePage';
import FAQSPage from './Pages/FAQS/FAQSPage'
import ForbiddenPage from './Pages/Forbiddem/ForbiddenPage';
import TermsConditionPage from './Pages/TermCondition/TermsConditionPage';
import ShippingRefundPage from './Pages/ShippingRefund/ShippingRefundPage';



const router = createBrowserRouter(
  createRoutesFromElements(
    <Route path="/" element={<Header />}>
      <Route index element={<Home />} />
      <Route path="login" element={<Login />} />
      <Route path="register" element={<Register />} />
      <Route path="cart" element={<CartPage />} />
      <Route path="about" element={<AboutPage />} />
      <Route path="checkout" element={<CheckOutPage />} />
      <Route path="/product/:id" element={<ProductDetails />} />
      <Route path="/search" element={<SearchPage />} />
      <Route path="/request-order" element={<ReqOrderFormPage />} />
      <Route path="/FAQS" element={<FAQSPage />} />
      <Route path="/forbidden_list" element={<ForbiddenPage />} />
      <Route path="/terms_condition" element={<TermsConditionPage />} />
      <Route path="/shipping_refund" element={<ShippingRefundPage />} />
      <Route path="/ShipForMe" element={<ShipForMePage />} />
        <Route path="/PayForMe" element={<PayForMePage />} /> 
      <Route path="/store" element={<StorePage />} />
      <Route path="myaccount" element={<MyAccountPage />}>
              <Route index element={<Dashboard />} />
              <Route path="order" element={<OrderPage />} />
              <Route path="Request-Orders" element={<RequestOrdersPage />} />
              <Route path="Shipping-Request" element={<ShippingRequestPage />} />
              <Route path="Payment-Request" element={<PaymentRequestPage />} />
              <Route path="Delivery" element={<DeliveryPage />} />
              <Route path="Ticket" element={<TicketPage />} />
              <Route path="Wallet" element={<Wallet />} />
            </Route>
            {/* <Route exact path="/search" component={CustomizedInputBase} /> */}
    </Route>
  )
)

function App() {

  return (
      <RouterProvider router={router}/>
   
  );
}

export default App;