import React from 'react'
import { Link } from 'react-router-dom';
import './static/css/ProductCard.css'
const ProductCardComponent = (product) => {

  return (
    <>
      <Link to={`/product/${product.product.product_no}`}>
        <div className="slideInner___2mfX9 !relative  carousel__inner-slide rounded" >
          {product.product.link && (
            <span
              className='absolute theme_color z-40 theme-colorl top top-0 right-0 text-white mt-1.5 mr-2 p-1 text-xs rounded-md shadow-md '
            >
              {product.product.link.startsWith('https://www.amazon.com/') || product.product.link.startsWith('https://a.co/') ? 'Amazon.com' : ''}
              {product.product.link.startsWith('https://www.alibaba.com') || product.product.link.startsWith('https://x.alibaba.com/') || product.product.link.startsWith('https://m.alibaba.com') ? 'Alibaba.com' : ''}
            </span>
          )}
          <div height="100%" className="sc-19ecb654-0 sc-47ca5f8e-0 fnvrHW bg-white shadow-md text-black rounded">
            <div className="sc-19ecb654-0 sc-47ca5f8e-1 kihmmo jfUrUf">

              <span style={{ boxSizing: 'border-box', display: 'block', overflow: 'hidden', width: 'initial', height: 'initial', background: 'none', opacity: 1, border: 0, margin: 0, padding: 0,  }}>
                <span style={{ boxSizing: 'border-box', display: 'block', width: 'initial', height: 'initial', background: 'none', opacity: 1, border: 0, margin: 0, padding: 0, paddingTop: '100%' }}></span>
                <img
                  src={product.product.image}
                  alt={product.product.name}
                  decoding="async"
                  data-nimg="responsive"
                  className="product-img rounded-t"
                  style={{
                    position: 'absolute',
                    top: 0,
                    left: 0,
                    bottom: 0,
                    right: 0,
                    boxSizing: 'border-box',
                    padding: 0,
                    border: 'none',
                    margin: 'auto',
                    display: 'block',
                    width: 0,
                    height: 0,
                    minWidth: '100%',
                    maxWidth: '100%',
                    minHeight: '100%',
                    maxHeight: '100%',
                    objectFit: 'cover'
                  }}
                  sizes="80vw"
                  srcSet={product.product.image}
                />
              </span>

              <button className="sc-d07c1f11-0 beguZC sc-47ca5f8e-2 ehFAkV product-actions">
                {/* SVG for eye icon */}
              </button>
              <button className="sc-d07c1f11-0 beguZC sc-47ca5f8e-3 bGaRqf product-actions">
                {/* SVG for heart icon */}
              </button>
            </div>
            <div className="sc-19ecb654-0 OwBmj text-center">
              <p className="mini-line ml-1 text-sm mt-2">{product.product.name}</p>
              <h4 style={{ fontWeight: 700, fontSize: '17px' }} className="sc-db80def1-0 ewuyNq mt-2 text-sm">৳ {product.product.price}</h4>
              
              <button className="p-2 border text-xs theme_color theme_colorl whitespace-nowrap mt-2 rounded-full  w-fit text-white shadow-md mb-2">
                View Detilas  </button>
            </div>
          </div>
        </div>

      </Link>
    </>
  )
}

export default ProductCardComponent