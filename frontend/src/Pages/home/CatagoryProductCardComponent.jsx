import React from 'react'
import ProductGrid from '../../components/FrontendTheme/ProductCatagoryGridComponent'
import { Link } from 'react-router-dom';
const CatagoryProductCardComponent = ({props}) => {
    if (!props) {
        return null; // or handle the loading state
      } 
    const category = props[Object.keys(props)[0]];
    const product = props[Object.keys(props)[1]];
    return (
        <div>
            <div className='grid grid-cols-1 lg:grid-cols-5 gap-4'>
                <div className='bg-white  flex flex-col shadow-md rounded  text-black p-4'>
                    
                    <span className='text-xl font-semibold'>{Object.keys(props)[0]}</span>
                    <div className='mt-2 mb-4 flex flex-col space-y-2 text-sm'>
                    {category.map((subcategory, subIndex) => (
              <span key={subIndex} className='cursor-pointer'>
                <Link to={`/search?query=${subcategory}`}>
                
                {subcategory}
                </Link>
              </span>
            ))}
                       
                    </div>
                <Link to={`/search?query=${Object.keys(props)[0]}`}>
                    <span className='mt-6 cursor-pointer'>Browse  All</span>
            </Link>
                </div>
                <div className='lg:col-span-4'>
                    <ProductGrid props={product}/>
                </div>
            </div>
          
        </div>
    )
}

export default CatagoryProductCardComponent