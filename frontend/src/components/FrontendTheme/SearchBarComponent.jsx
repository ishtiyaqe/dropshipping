import React, { useState } from 'react';
import Paper from '@mui/material/Paper';
import InputBase from '@mui/material/InputBase';
import IconButton from '@mui/material/IconButton';
import SearchIcon from '@mui/icons-material/Search';
import { useNavigate } from 'react-router-dom';
import clients from '../api/Client';
import LoadingBar from 'react-top-loading-bar'




export default function CustomizedInputBase() {
  const [searchQuery, setSearchQuery] = useState('');
  const navigate = useNavigate();
  const [progress, setProgress] = useState(0)

  const handleSearch = () => {
    setProgress(10);
    // e.preventDefault();
    // Get the search query from the form input field (assuming you have an input field with the name 'searchQuery')
    setProgress(60);
  
    // Make an API request to your Django view with the search query
    clients
      .get(`/search/?query=${searchQuery}`)
      .then((response) => {
        
        // Check if the response contains 'products' property
        if (Array.isArray(response.data.products) && response.data.products.length === 1) {
          const product_no =  response.data.products[0].product_no; // Log products data
          // Use history.push to navigate to the search URL with the search query
          setProgress(100);
          navigate(`/product/${product_no}`)
        } else {
          setProgress(100);
          navigate(`/search?query=${searchQuery}`);
          window.location.reload();
        }
      })
      .catch((error) => {
        console.error('Error:', error);
      });
  };
  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      // Trigger search when Enter key is pressed
      handleSearch();
    }
  };

  
  return (
    <>
     <LoadingBar
        color='#f11946'
        progress={progress}
        onLoaderFinished={() => setProgress(0)}
      />


    <Paper
      component="form"
      sx={{ p: '2px 4px', display: 'flex', alignItems: 'center', borderRadius: 25, width: '100%' }}
    >
      
      <InputBase
        sx={{ ml: 1, flex: 1 }}
        placeholder="Search For products"
        inputProps={{ 'aria-label': 'Search For products' }}
        value={searchQuery}
        onChange={(e) => setSearchQuery(e.target.value)}
        onKeyDown={handleKeyPress}
      />
      <IconButton type="button" sx={{ p: '10px' }} aria-label="search" onClick={handleSearch}>
        <SearchIcon />
      </IconButton>
    </Paper>
    </>
  );
}
