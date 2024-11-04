import React, { useEffect, useState } from 'react';
import Skeleton from '@mui/material/Skeleton';
import Stack from '@mui/material/Stack';
import { bgcolor } from '@mui/system';
import clients from '../../components/api/Client';
import { useNavigate } from 'react-router-dom';
import ProductCardComponent from '../../components/FrontendTheme/ProductCardComponent';
import LoadingBar from 'react-top-loading-bar';
import notinhfound from '../../assets/9264822-removebg-preview.png';
import { Link } from 'react-router-dom';

// Define your SearchPage component
function SearchPage() {
    const [progress, setProgress] = useState(0);
    const [products, setProducts] = useState([]);
    const [query, setQuery] = useState(
        new URLSearchParams(window.location.search).get('query') || ''
    );
    const [searchStatus, setSearchStatus] = useState('');
    const [requestCounter, setRequestCounter] = useState(0);
    const navigate = useNavigate();
    const [isLoading, setIsLoading] = useState(true);

    

    useEffect(() => {
        const fetchData = async () => {
            
            try {
                const productsResponse = clients.get(`/search/?query=${query}`);
                if (productsResponse.data.products && Array.isArray(productsResponse.data.products)) {
                    const mappedProducts = productsResponse.data.products.map(item => ({
                        id: item.id,
                        product_no: item.product_no,
                        name: item.name,
                        image: item.image,
                        price: item.price ? parseFloat(item.price) : 0,
                    }));
                    setProducts(mappedProducts);
                    setIsLoading(false);
                    clearInterval(intervalId);
                } else {
                    console.log(productsResponse.data);
                }
            } catch (error) {
                console.log();
            }

            if (query) {
                try {
                    const response = await clients.get(`/check_search_status/?query=${query}`);
                    const data = response.data;
                    setRequestCounter(requestCounter + 1);
                    setSearchStatus(data.status);

                    if (data.status === 'Completed') {
                        try {
                            const productsResponse = await clients.get(`/searchComplete/?query=${query}`);
                            if (productsResponse.data.products && Array.isArray(productsResponse.data.products)) {
                                const mappedProducts = productsResponse.data.products.map(item => ({
                                    id: item.id,
                                    product_no: item.product_no,
                                    name: item.name,
                                    image: item.image,
                                    price: item.price ? parseFloat(item.price) : 0,
                                }));
                                setProducts(mappedProducts);
                                setIsLoading(false);
                                clearInterval(intervalId);
                            } else {
                                console.log(productsResponse.data);
                            }
                        } catch (error) {
                            console.log(error);
                        }
                    }
                } catch (error) {
                    console.error(error);
                }
            }
        };

        const intervalId = setInterval(fetchData, 3000);
        // Check if the counter has reached 20 and the status is "Completed" to navigate to the home page
        if (requestCounter === 80 && searchStatus === 'Searching') {
            clearInterval(intervalId);
            navigate('/request-order'); // Navigate to the home page
        }
       

        // Cleanup the interval when the component unmounts
        return () => {
            clearInterval(intervalId);
        };
    }, [query,requestCounter, navigate,searchStatus ]);

    return (
        <div>
            <LoadingBar color='#f11946' progress={progress} onLoaderFinished={() => setProgress(0)} />
            {isLoading ? (
                // Show a loading or skeleton UI here
                <>
                    <div className="skeleton-loader grid  grid-cols-2 gap-4 m-6 lg:hidden">
                        <Stack spacing={1} sx={bgcolor}>
                            <Skeleton variant="rectangular" width={200} height={160} />
                            <Skeleton variant="rectangular" width={80} height={30} />
                            <Skeleton variant="rectangular" width={90} height={20} />
                        </Stack>
                        <Stack spacing={1} sx={bgcolor}>
                            <Skeleton variant="rectangular" width={200} height={160} />
                            <Skeleton variant="rectangular" width={80} height={30} />
                            <Skeleton variant="rectangular" width={90} height={20} />
                        </Stack>
                        <Stack spacing={1} sx={bgcolor}>
                            <Skeleton variant="rectangular" width={200} height={160} />
                            <Skeleton variant="rectangular" width={80} height={30} />
                            <Skeleton variant="rectangular" width={90} height={20} />
                        </Stack>
                        <Stack spacing={1} sx={bgcolor}>
                            <Skeleton variant="rectangular" width={200} height={160} />
                            <Skeleton variant="rectangular" width={80} height={30} />
                            <Skeleton variant="rectangular" width={90} height={20} />
                        </Stack>
                    </div>
                    <div className="skeleton-loader lg:grid lg:grid-cols-4 grid-cols-2 gap-4 m-6 hidden">
                        <Stack spacing={1} sx={bgcolor}>
                            <Skeleton variant="rectangular" width={210} height={160} />
                            <Skeleton variant="rectangular" width={140} height={30} />
                            <Skeleton variant="rectangular" width={180} height={20} />
                        </Stack>
                        <Stack spacing={1} sx={bgcolor}>
                            <Skeleton variant="rectangular" width={210} height={160} />
                            <Skeleton variant="rectangular" width={140} height={30} />
                            <Skeleton variant="rectangular" width={180} height={20} />
                        </Stack>
                        <Stack spacing={1} sx={bgcolor}>
                            <Skeleton variant="rectangular" width={210} height={160} />
                            <Skeleton variant="rectangular" width={140} height={30} />
                            <Skeleton variant="rectangular" width={180} height={20} />
                        </Stack>
                        <Stack spacing={1} sx={bgcolor}>
                            <Skeleton variant="rectangular" width={210} height={160} />
                            <Skeleton variant="rectangular" width={140} height={30} />
                            <Skeleton variant="rectangular" width={180} height={20} />
                        </Stack>
                    </div>
                </>
            ) : products.length > 0 ? (
                <section className="py-12">
                    {/* Add your content here */}
                    <div className="container max-w-screen-xl mx-auto px-4">
                        <div className="flex flex-col md:flex-row -mx-4">
                            <main className="md:w-3/3 lg:w-4/4 px-4">
                                <div className="grid grid-cols-2 sm:grid-cols-2 md:grid-cols-4 lg:grid-cols-5 gap-4">
                                    {products.map((item, index) => (
                                        <div key={index}>
                                            <ProductCardComponent product={item} />
                                        </div>
                                    ))}
                                </div>
                            </main>
                        </div>
                    </div>
                </section>
            ) : (
                <>
                    <img src={notinhfound} className='flex justify-center m-auto' alt="" />
                    <p className='p-6 text-center text-3xl font-sem'>No products to display</p>
                    <button className="flex justify-center m-auto mb-10 theme_color theme_colorl p-4 text-white rounded-md shadow-md">
                        <Link to="/store">
                            Return to Shop
                        </Link>
                    </button>
                </>
            )}
        </div>
    );
}

export default SearchPage;
