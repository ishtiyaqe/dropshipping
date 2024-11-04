import React, { useState, useEffect } from 'react';
import clients from '../../components/api/Client';
import Skeleton from '@mui/material/Skeleton';


function ColorComponent(props) {
  const { productNo, onColorChange, activeColor, setActiveColor, selectedImage, onImageChange } = props;

  const [colors, setColors] = useState([]);
  const [colorss, setColorss] = useState('');
  const [loading, setLoading] = useState(true);
  const [isExpanded, setIsExpanded] = useState(false);
  // Maximum number of colors to show initially
  const maxVisibleColors = 7;

  const visibleColors = isExpanded ? colors : colors.slice(0, maxVisibleColors);

  const toggleExpand = () => {
    setIsExpanded(!isExpanded);
  };


  useEffect(() => {
    const fetchColorData = async () => {
      try {
        const response = await clients.get(`/get_color/${productNo}`);
        const colorData = response.data.sizes;
        setColors(colorData);
        setLoading(false);

        if (colorData.length > 0) {
          if (!colorData.some((color) => color.color === activeColor)) {
            setActiveColor(colorData[0].color);
            setColorss(colorData[0].color);
          }
        }
      } catch (error) {
        console.error('Error fetching color data:', error);
      }
    };

    fetchColorData();
  }, [productNo, onColorChange, activeColor, setActiveColor]);
useEffect(() => {
  

  setActiveColor(colorss);
  
}, [colorss, setActiveColor])

  const handleColorClick = (color, image) => {
    setActiveColor(color);
    onColorChange(color);
    onImageChange(image);
  };

  return (
    <div >
      {loading ? (
        <div className="grid lg:grid-cols-5 grid-cols-4 gap-2">
          <Skeleton variant="rectangular" width={80} height={80} />
          <Skeleton variant="rectangular" width={80} height={80} />
          <Skeleton variant="rectangular" width={80} height={80} />
          <Skeleton variant="rectangular" width={80} height={80} />
          <Skeleton variant="rectangular" width={80} height={80} />
        </div>
      ) : (
        <div>
          {colors.length > 0 ? (
            activeColor ? (
             
< div >
            <span>Color: {activeColor}</span>
            <div className="grid lg:grid-cols-5 grid-cols-4 gap-2">
      {visibleColors.map((color, index) => (
        <div className="w-full" key={index}>
          <div
            className={`color-item flex justify-center ${color.color === activeColor ? 'active' : ''}`}
            onClick={() => handleColorClick(color.color, color.image)}
          >
            {color.image !== 'None' ? (
              <div>
                <img
                  src={color.image}
                  alt={color.color}
                  style={{ width: '80px', height: '80px' }}
                  className="cursor-pointer object-fit rounded shadow-md"
                />

              </div>
            ) : (
              <div>
                <div
                  className={`color-name ${color.color === activeColor ? 'active' : ''}`}
                  onClick={() => handleColorClick(color.color, null)}
                >
                  <span className="p-2 flex  text-xs overflow-clip cursor-pointer  border rounded-md shadow-md dark:shadow-gray-200">
                    {color.color}
                  </span>
                </div>
              </div>
            )}
          </div>
        </div>
      ))}
      {colors.length > maxVisibleColors && (
        <div className="w-full flex justify-center">
          <button className="theme_color theme_colorl rounded-md shadow-md text-white lg:text-md text-xs p-2" onClick={toggleExpand}>
            {isExpanded ? 'Show Less' : 'Show More'}
          </button>
        </div>
      )}
    </div>
            </div>
            ) : (
              <></>
            )
            
      ):(
      <></>
          )}
    </div>
  )
}
    </div >
  );
}

export default ColorComponent;
