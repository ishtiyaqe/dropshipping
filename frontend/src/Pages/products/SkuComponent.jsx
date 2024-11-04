import React, { useState, useEffect } from 'react';
import clients from '../../components/api/Client';
import Skeleton from '@mui/material/Skeleton';

const SkuComponent = ({ productNo, onColorChange, onImageChange }) => {
  const [Sku, setSku] = useState([]);
  const [loading, setLoading] = useState(true);
  const [activeSku, setActiveSKU] = useState(null);
  const [groupedColors, setGroupedColors] = useState({});

  useEffect(() => {
    const fetchColorData = async () => {
      try {
        const response = await clients.get(`/get_Sku/${productNo}`);
        const colorData = response.data.Sku;

        // Organize colors by SKU name
        const grouped = colorData.reduce((acc, Sku) => {
          acc[Sku.name] = acc[Sku.name] || [];
          acc[Sku.name].push(Sku);
          return acc;
        }, {});
        setGroupedColors(grouped);
        setLoading(false);

      } catch (error) {
        console.error('Error fetching color data:', error);
      }
    };

    fetchColorData();
  }, [productNo]);

  const handleColorChange = (name) => {
    // Set active color based on the selected name
    const defaultOption = groupedColors[name][0].option;
    const selectedColor = { name, option: defaultOption };

    setActiveSKU(selectedColor.option);
    // onColorChange(selectedColor.name);
    // onImageChange(selectedColor.option);
  };

  return (
    <div className="flex flex-col">
      {loading ? (
        <div>
          <Skeleton variant="rectangular" width={400} height={40} />
        </div>
      ) : groupedColors ? (
        <div>
         
        </div>
      ) : (
        <div className="w-full text-sm flex flex-col space-y-2">
          <label htmlFor="colorSelect">Select Color: {activeSku}</label>
          <select
            className='p-4 bg-white rounded shadow-md dark:shadow-gray-200 text-black'
            id="colorSelect"
            value={activeSku ? activeSku.name : ''}
            onChange={(e) => handleColorChange(e.target.value)}
          >
            <option value="" disabled>Select a color</option>
            {Object.keys(groupedColors).map((groupName, index) => (
              <optgroup key={index} label={groupName}>
                {groupedColors[groupName].map((color, colorIndex) => (
                  <option key={colorIndex} value={color.name}>
                    {color.name}: {color.option}
                  </option>
                ))}
              </optgroup>
            ))}
          </select>
        </div>
        
      )}
    </div>
  );
};

export default SkuComponent;
