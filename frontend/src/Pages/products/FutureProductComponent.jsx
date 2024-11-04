import React from 'react'
import ProductGrid from '../../components/FrontendTheme/ProductGridComponent'
const FutureProductComponent = () => {
  return (
    <div>
        <div>
          <span className='m-2 text-xl font-black '>Featured Products</span>
          <hr className='  mb-4 border-2' />
          <ProductGrid />
        </div>
    </div>
  )
}

export default FutureProductComponent