import React, { useEffect, useState } from 'react';
import clients from '../api/client';

const SubcategoriesComponent = () => {
  const [categories, setCategories] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await clients('/subcategories/');
        const data = await response.json();
        setCategories(data);
      } catch (error) {
        console.error('Error fetching subcategories:', error);
      }
    };

    fetchData();
  }, []);

  return (
    <div>
      {categories.map((category, index) => (
        <div key={index}>
          <h3>{Object.keys(category)[0]}</h3>
          <ul>
            {category[Object.keys(category)[0]].map((subcategory, subIndex) => (
              <li key={subIndex}>{subcategory}</li>
            ))}
          </ul>
        </div>
      ))}
    </div>
  );
};

export default SubcategoriesComponent;
