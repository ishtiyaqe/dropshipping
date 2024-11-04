import React, { useEffect, useState } from 'react';
import Skeleton from '@mui/material/Skeleton';
import clients from '../components/api/client';
import { Link } from 'react-router-dom';

const Footer = () => {
  const [categories, setCategories] = useState([]);
  const [footerLinks, setFooterLInkss] = useState([]);
  const [paymentLogo, setPaymentLogo] = useState([]);


  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await clients.get('/FooterWidgets/');
        const ftrlinks = await clients.get('/FooterLinks/');
        const ptl = await clients.get('/FooterPaymentSuportImage/');
        const data = await response.data.Footer_weidgt;
        const linksdata = await ftrlinks.data.Footer_links;
        const data1 = await ptl.data.Home_banner.image;
        setFooterLInkss(linksdata)
        setCategories(data);
        setPaymentLogo(data1)
      } catch (error) {
        console.error('Error fetching subcategories:', error);
      }
    };

    fetchData();
  }, [setCategories])


  return (
    <footer className="bg-black  h-full">
      {/* section footer top */}

      {/* section footer top end */}
      {/* section footer top */}
      <div className="grid container lg:grid-cols-3 grid-cols-1  gap-2 p-4 mt-4">
        <div >
          <section className="  text-white flex lg:hidden">
            <div className=" ">
              <div className="flex flex-wrap">
                <aside className="">
                  <a href="/">
                    <div className="justify-items-center list-group-item">
                      <div className="wrap p-2 r" id="picture">
                        <img
                          alt=" "
                          className="h-10 w-auto"
                          src={categories.image}
                        />
                        <div className="p-1"></div>
                        <div dangerouslySetInnerHTML={{ __html: categories.slogan }} />

                      </div>
                    </div>
                  </a>
                </aside>

                {/* Add the other 'aside' elements similarly */}
              </div>
            </div>
          </section>
          <section className=" text-white hidden lg:flex">
            <div className="">
              <div className="flex flex-wrap">
                <aside className="">
                  <a href="/">
                    <div className="">
                      <div className="wrap p-2 r" id="picture">
                        <img
                          alt=" "
                          className="mt-3 w-34 mr-2 h-8"
                          src={categories.image}
                        />
                        <div  dangerouslySetInnerHTML={{ __html: categories.slogan }} />
                      </div>
                    </div>
                  </a>
                </aside>

                {/* Add the other 'aside' elements similarly */}
              </div>
            </div>
          </section>

        </div>
        <div className="lg:col-span-2 text-white">
          <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 m-4 ">
            {footerLinks.map((subcategory, subIndex) => (

              <div className='p-4 cursor-pointer whitespace-wrap' key={subIndex}>
                <Link to={subcategory.url}>
                {subcategory.name}
                
                </Link>
                </div>
            ))}

          </div>
        </div>
      </div>
      {/* section footer top end */}
      {/* section footer bottom  */}
      <section className="bg-black py-6 text-white flex justify-center m-auto text-center">
        <div className="c">
          <div className="lg:flex justify-center">
            <div className="mb-1 ml-14">
              <img
                src={paymentLogo}
                className="w-32 h-10"
                alt="Payment methods"
              />
            </div>
            <div className="space-x-6 self-center">
              <p className="my-4 lg:mb-1 mb-12">
                <a target="_blank" href="https://unicornitpark.com/">
                  Design & Developed by Unicorn It Park
                </a>
              </p>
            </div>
          </div>
        </div>
      </section>
      {/* section footer bottom  end */}
    </footer>
  );
};

export default Footer;
