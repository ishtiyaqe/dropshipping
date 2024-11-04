import React, { useState, useEffect } from 'react';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import AddIcon from '@mui/icons-material/Add';
import { useNavigate } from 'react-router-dom';
import clients from '../../components/api/Client';
import DeleteIcon from '@mui/icons-material/Delete';
import ShipForMeProcessCard from './PayForMeProcessCard'

const PayForMePage = () => {
  const [currentUser, setCurrentUser] = useState(true); // Set an initial value for currentUser

  const navigate = useNavigate();
 


  const [requestSections, setRequestSections] = useState([{
    product_name: '',
    product_link: '',
      quantity: '',
      color: '',
      message: '',
      product_image: '',
  }]);

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
            product_name: '',
    product_link: '',
      quantity: '',
      color: '',
      message: '',
      product_image: '',
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
      
          message: section.message,
          product_name: section.product_name,
          product_link: section.product_link,
      quantity: section.quantity,
      color: section.color,
      product_image: section.product_image,
      }));
      for (const sectionData of allSectionsData) {
          // Use clients.post to send the data for each section individually
          await clients
              .post('api/Paysforme/', sectionData)
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
                                      type="text"
                                      label="Product Name"
                                      name="product_name"
                                      value={section.product_name || ''}
                                      onChange={(e) => handleInputChange(e, index)}
                                      variant="outlined"
                                      margin="normal"
                                      
                                  />
                                  <TextField
                                      required
                                      type="text"
                                      label="Product Link"
                                      name="product_link"
                                      value={section.product_link || ''}
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
                                          required
                                          type="text"
                                          label="Color/Size"
                                          name="color"
                                          value={section.color || ''}
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
                          <span className="text-lg  font-semibold grid grid-cols-4 justify-center ml-auto mr-auto  lg:grid-cols-4 lg:gap-16 gap-4  ">

                              <ShipForMeProcessCard />
                          </span>
                      </div>
                  </div>
                 

              </div>

          </div>
      </>
  );
};

export default PayForMePage