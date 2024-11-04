import React, { useState, useEffect } from 'react';
import clients from '../../components/api/Client';
import Skeleton from '@mui/material/Skeleton';

const DescriptionComponent = ({ productNo }) => {
  const [description, setDescription] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchColorData = async () => {
      try {
        const response = await clients.get(`/productdescription/${productNo}`);
        const descriptionData = response.data.descriptions;
  
        if (descriptionData.length === 0) {
          setError("No description found");
        } else {
          setDescription(descriptionData);
        }
  
        setLoading(false);
      } catch (error) {
        console.error('Error fetching color data:', error);
        setError("An error occurred while fetching data");
        setLoading(false);
      }
    };
  
    fetchColorData();
  }, [productNo]);
  

  return (
    <div className=' space-y-4'>
      {loading && <Skeleton animation="wave" height={100} />}
      {error && <p className='text-xl text-center p-4'>{error}</p>}
      {!loading && !error && description.map((item, index) => (
        <div key={index}>
          {/* Render your description data here */}
          <img className='p-4 w-full h-full border' src={item.des} alt={item.id} />
          
        </div>
      ))}
    </div>
  );
};

export default DescriptionComponent;
