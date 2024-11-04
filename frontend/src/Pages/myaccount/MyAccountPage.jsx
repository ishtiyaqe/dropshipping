import React, { useEffect, useState } from 'react'
import AccountLayout from './AccountLayout'
import { useNavigate } from 'react-router-dom';
import clients from '../../components/api/Client';



export const MyAccountPage = () => {
  const [currentUser, setCurrentUser] = useState();
  const navigate = useNavigate();
  useEffect(() => {
    clients.get("/api/user")
      .then(function (res) {
        setCurrentUser(true);
      })
      .catch(function (error) {
        setCurrentUser(false);
        navigate('/login');
      });
  }, [currentUser, navigate]);
  return (
    <>
      <div className=''>
   
          <AccountLayout />
       
      </div>
    </>
  )
}
export default MyAccountPage