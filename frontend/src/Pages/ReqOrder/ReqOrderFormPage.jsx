import React, { useState, useEffect } from 'react';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import AddIcon from '@mui/icons-material/Add';
import { useNavigate } from 'react-router-dom';
import clients from '../../components/api/Client';
import DeleteIcon from '@mui/icons-material/Delete';
import RqoProcesBard from './RqoProcesBard'

const ReqOrderFormPage = () => {
    const [currentUser, setCurrentUser] = useState(true); // Set an initial value for currentUser
    const [showMessage1, setShowMessage1] = useState(true);
    const [showMessage2, setShowMessage2] = useState(false);
    const [ShippngDetails, setShippngDetails] = useState([]);
    const [ShippngCharge, setShippngCharge] = useState([]);
    const [ShippngMessage, setShippngMessage] = useState([]);
    const navigate = useNavigate();
    useEffect(() => {
        clients
            .get("/api/shipformedes/")
            .then(function (res) {
                setShippngDetails(res.data[0]);
                
            })
            .catch(function (error) {
                
                // Redirect to the login page if there's no currentUser
            });
        clients
            .get("/api/shipformecharge/")
            .then(function (res) {
                setShippngCharge(res.data[0]);
                
            })
            .catch(function (error) {
                
                // Redirect to the login page if there's no currentUser
            });
        clients
            .get("/api/shipformemesssages/")
            .then(function (res) {
                setShippngMessage(res.data[0]);
                
            })
            .catch(function (error) {
                
                // Redirect to the login page if there's no currentUser
            });
    }, [])

    const toggleMessage = (messageNumber) => {
        if (messageNumber === 1) {
            setShowMessage1((prev) => !prev);
            setShowMessage2(false);
        } else if (messageNumber === 2) {
            setShowMessage2((prev) => !prev);
            setShowMessage1(false);
        }
    };
    const [requestSections, setRequestSections] = useState([{
        link: '',
        title: '',
        quantity: '',
        message: '',
        image: '',
    }]);
    const toggleDiv = () => {
        setShowFirstDiv((prev) => !prev);
    };
    useEffect(() => {
        clients
            .get("/api/user")
            .then(function (res) {
                setCurrentUser(true);
                
            })
            .catch(function (error) {
                setCurrentUser(false);
                
                navigate('/login');
            });
    }, [currentUser]);



    const handleInputChange = (e, index) => {
        const { name, value } = e.target;
        setRequestSections((prevSections) => {
            const updatedSections = [...prevSections];
            updatedSections[index] = {
                ...updatedSections[index],
                [name]: value,
            };
            return updatedSections;
        });
    };

    const createNewRequestSection = () => {
        if (requestSections.length < 100) {
            setRequestSections([...requestSections, {
                link: '',
                title: '',
                quantity: '',
                message: '',
                image: '',
            }]);
        }
    };

    const removeRequestSection = (index) => {
        setRequestSections((prevSections) => prevSections.filter((_, i) => i !== index));
    };


    const handleSubmit = async (e) => {
        e.preventDefault();

        // Combine all form sections into an array to send in a single request
        const allSectionsData = requestSections.map((section) => ({
            link: section.link,
            title: section.title,
            quantity: section.quantity,
            message: section.message,
            image: section.image,
        }));
        for (const sectionData of allSectionsData) {
            // Use clients.post to send the data for each section individually
            await clients
                .post('api/rqo/', sectionData)
                .then(function (res) {
                    
                    navigate('/myaccount/Request-Orders');
                })
                .catch(function (error) {
                    console.error("Error submitting requests:", error);
                });
            // Optionally, handle the response for each section if needed
        }
        // Use clients.post to send the data for all sections

    };

    return (
        <>
            <div className='grid lg:grid-cols-2 grid-cols-1 gap-2'>
                <div>
                    <div>
                        {/* Render the form */}
                        {requestSections.map((section, index) => (
                            <div key={index} className='w-full p-2 lg:p-4'>
                                <form className='flex flex-col p-2' onSubmit={(e) => handleSubmit(e, section)}>
                                    <TextField
                                        required
                                        type="url"
                                        label="Link"
                                        name="link"
                                        value={section.link || ''}
                                        onChange={(e) => handleInputChange(e, index)}
                                        variant="outlined"
                                        margin="normal"
                                    />
                                    <TextField
                                        required
                                        type="text"
                                        label="Title"
                                        name="title"
                                        value={section.title || ''}
                                        onChange={(e) => handleInputChange(e, index)}
                                        variant="outlined"
                                        margin="normal"
                                    />
                                    <TextField
                                        required
                                        type="number"
                                        label="Quantity"
                                        name="quantity"
                                        value={section.quantity || ''}
                                        onChange={(e) => handleInputChange(e, index)}
                                        variant="outlined"
                                        margin="normal"
                                    />
                                    <TextField
                                        label="Message"
                                        name="message"
                                        value={section.message || ''}
                                        onChange={(e) => handleInputChange(e, index)}
                                        variant="outlined"
                                        margin="normal"
                                        multiline
                                        rows={4}
                                        required
                                    />
                                    <input
                                        type="file"
                                        id={`transactionImage-${index}`}
                                        accept="image/*"
                                        name="image"
                                        className='overflow-hidden mb-4'
                                    />
                                    <div className='flex justify-center space-x-4 m-4 lg:text-md text-xs text-center'>
                                        <button
                                            className='bg-red-600 p-4 text-white rounded-full shadow-md dark:shadow-gray-200'
                                            type="button"
                                            onClick={() => removeRequestSection(index)}
                                        >
                                            <DeleteIcon />
                                        </button>
                                    </div>
                                </form>
                            </div>
                        ))}
                        <div className='flex justify-center space-x-4 m-4 lg:text-md text-xs text-center'>

                            <button
                                variant="contained"
                                color="primary"
                                className='bg-gray-400 p-4 rounded-full text-gray-950'
                                onClick={createNewRequestSection}
                            >
                                <AddIcon />
                                Add Another Request
                            </button>

                            <button
                                className='theme_color theme_colorl thme_colorl p-4 text-white rounded-full '
                                type="button"
                                onClick={handleSubmit}
                            >
                                Submit All Requests
                            </button>

                        </div>
                        {/* Add a button to create a new form section */}
                    </div>

                </div>
                <div className='w-full p-4 flex  flex-col'>
                    <div className='flex justify-center '>

                        <div className="">
                            <span className="text-lg  font-semibold grid grid-cols-3 lg:grid-cols-6 lg:gap-16 gap-4 lg:mr-8 mr-0 ">

                                <RqoProcesBard />
                            </span>
                        </div>
                    </div>
                    <div className="p-4 flex justify-center bg-gray-200 rounded-md shadow-md mt-4 mb-4">
                        <span className="text-lg font-semibold">
                            <div className='flex justify-end ml-auto w-full'>

                                <button className='p-2 w-32 theme_color theme_colorl rounded-full shadow-md m-2 text-white drop-shadow-md' onClick={() => toggleMessage(1)}>
                                    China
                                </button>
                                <button className='p-2 w-32 theme_color theme_colorl rounded-full shadow-md m-2 text-white drop-shadow-md' onClick={() => toggleMessage(2)}>
                                    USA
                                </button>
                            </div>


                            {showMessage1 && (
                                <div className=" flex text-black w-full justify-center  mt-4 mb-4">
                                    <span className="text-lg font-semibold">
                                        <div className="flex justify-center w-full text-center">

                                            <div className='grid grid-cols-1 w-full'>

                                                <span className="p-4 border text-sm border-gray-950">
                                                    Shipping Rate
                                                </span>
                                                <span className="p-4 border-b border-l text-xs border-gray-950">
                                                   ৳ {ShippngCharge.China_charge}
                                                </span>
                                            </div>
                                            <div className='grid grid-cols-1 w-full'>

                                                <span className="p-4 border-b text-sm border-r border-t border-gray-950">
                                                    Shipping Time
                                                </span>
                                                <span className="p-4 text-xs border-b border-l border-r border-gray-950">
                                                    {ShippngCharge.China_days}
                                                </span>
                                            </div>
                                        </div>
                                        <div className=" p-4  border-r border-l  border-gray-950 text-xs">
                                            Shipping Details: {ShippngDetails.China}
                                       
                                        </div>
                                        <div className=" p-4  border border-gray-950 text-xs">
                                       
                                        Shipping Messsage: {ShippngMessage.China}
                                        </div>

                                    </span>
                                </div>
                            )}

                            {showMessage2 && (
                                 <div className=" flex text-black w-full justify-center  mt-4 mb-4">
                                 <span className="text-lg font-semibold">
                                     <div className="flex justify-center w-full text-center">

                                         <div className='grid grid-cols-1 w-full'>

                                             <span className="p-4 border text-sm border-gray-950">
                                                 Shipping Rate
                                             </span>
                                             <span className="p-4 border-b border-l text-xs border-gray-950">
                                                ৳ {ShippngCharge.USA_charge}
                                             </span>
                                         </div>
                                         <div className='grid grid-cols-1 w-full'>

                                             <span className="p-4 border-b text-sm border-r border-t border-gray-950">
                                                 Shipping Time
                                             </span>
                                             <span className="p-4 text-xs border-b border-l border-r border-gray-950">
                                             {ShippngCharge.USA_days}
                                             </span>
                                         </div>
                                     </div>
                                     <div className=" p-4  border-r border-l  border-gray-950 text-xs">
                                         Shipping Details: {ShippngDetails.USA}
                                    
                                     </div>
                                     <div className=" p-4  border border-gray-950 text-xs">
                                    
                                     Shipping Messsage: {ShippngMessage.USA}
                                     </div>

                                 </span>
                             </div>
                               
                            )}
                        </span>
                    </div>

                </div>

            </div>
        </>
    );
};

export default ReqOrderFormPage;
