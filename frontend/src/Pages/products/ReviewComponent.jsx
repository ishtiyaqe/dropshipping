import React, { useState, useEffect } from 'react';
import clients from '../../components/api/Client';
import Skeleton from '@mui/material/Skeleton';

const ReviewComponent = ({ productNo }) => {
  const [Reviews, setReviews] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchColorData = async () => {
      try {
        const response = await clients.get(`/getReview/${productNo}`);
        const ReviewssData = response.data.reviews;

        // if (descriptionData.length === 0) {
        //   setError("Product description not found");
        // } else {
        //   setDescription(descriptionData);
        // }
        if (ReviewssData.length === 0) {
          setError("No Review Found");
          setLoading(false);
        } else {
          setReviews(ReviewssData);
          setLoading(false);
        }
      } catch (error) {
        console.error('Error fetching color data:', error);
        setError("No Review Found");
        setLoading(false);
      }
    };

    fetchColorData();
  }, [productNo]);

  return (
    <div className='space-y-4 p-2'>
      {loading && <Skeleton animation="wave" height={100} />}
      {error && <p className='text-center'>{error}</p>}
      {!Reviews && <p className='text-center'>No Review found!</p>}
      {!loading && !error && Reviews.map((item, index) => (
        <div key={index} className='p-4  border-2 rounded-md'>
          {/* Render your description data here */}
          <div className="flex justify-between">
            <span className='text-sm'>{item.Buyer_name}</span>
            {item.Country?.startsWith('//s.alicdn') ? (
  <img className='w-8 h-6' src={item.Country} alt="Country Flag" />
) : (
  <span className="text-sm">{item.Country}</span>
)}



          </div>
          <hr className='mt-2 mb-2' />
          <div className='flex flex-col'>


            <span className='text-sm'>  {item.Review_time}</span>
            <span className='text-md text-center'>{item.Review_text}</span>



          </div>
        </div>
      ))}
    </div>
  );
};

export default ReviewComponent;
