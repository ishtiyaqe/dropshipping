import React from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Layout from "./Layout";
import HomePage from "./home/HomePage";
import AboutPage from "./Abouutus/AboutPage";
import CartPage from "./cart/CartPage";
import ProductGrid from "../components/FrontendTheme/ProductGridComponent";
import ProductDetails from "./products/ProductDetailsPage";
import MyAccountPage from "./myaccount/MyAccountPage";
import Dashboard from "./myaccount/dashboard/Dashboard";
import OrderPage from "./myaccount/order/OrderPage";
import RequestOrdersPage from "./myaccount/RequestOrders/RequestOrdersPage";
import PaymentRequestPage from "./myaccount/PaymentRequest/PaymentRequestPage";
import ShippingRequestPage from "./myaccount/ShippingRequest/ShippingRequestPage";
import DeliveryPage from "./myaccount/Delivery/DeliveryPage";
import TicketPage from "./myaccount/Ticket/TicketPage";
import Wallet from "./myaccount/Wallet/WalletPage";
import SearchPage from "./search/SearchPage";
import StorePage from "./shop/ShopPage";
import ReqOrderFormPage from './ReqOrder/ReqOrderFormPage';
import ShipForMePage from './ShipForme/ShipForMePage';
import PayForMePage from './PayForMe/PayForMePage';
import FAQSPage from './FAQS/FAQSPage'
import ForbiddenPage from "./Forbiddem/ForbiddenPage";
import TermsConditionPage from "./TermCondition/TermsConditionPage";
import ShippingRefundPage from "./ShippingRefund/ShippingRefundPage";


const App = () => {
  return (
    <BrowserRouter>
      <Routes>
        <div className="container flex justify-center flex-col">
          <Route path="/" element={<Layout />}>
            <Route path="/" element={<HomePage />} />
            <Route path="/about" element={<AboutPage />} />
            <Route path="/cart" element={<CartPage />} />
            <Route path="/store" element={<StorePage />} />
            <Route path="/search" element={<SearchPage />} />
            <Route path="/request-order" element={<ReqOrderFormPage />} />
            <Route path="/ShipForMe" element={<ShipForMePage />} />
            <Route path="/FAQS" element={<FAQSPage />} />
            <Route path="/forbidden_list" element={<ForbiddenPage />} />
            <Route path="/terms_condition" element={<TermsConditionPage />} />
            <Route path="/shipping_refund" element={<ShippingRefundPage />} />
            <Route path="/PayForMe" element={<PayForMePage />} />
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
            <Route path="/product/:id" element={<ProductDetails />} />
</Route>
        </div>
      </Routes>
    </BrowserRouter>
  );
};

export default App;