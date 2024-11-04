import React, { useState, useEffect } from 'react';
import { Typography, Grid, TextField, FormControlLabel, Checkbox, Button } from '@mui/material';
import { useFetcher, useNavigate } from 'react-router-dom';
import EditLocationAltTwoToneIcon from '@mui/icons-material/EditLocationAltTwoTone';
import clients  from '../../components/api/Client'


export default function AddressForm(props) {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const navigate = useNavigate();
  const { setAddress, handleNext } = props
  const [isEditing, setIsEditing] = useState(false);
  const [formData, setFormData] = useState({
    full_name: '',
    phone: '',
    address: '',

  });
  
useEffect(() => {
  setAddress(formData)


}, [formData])

  
  const handleChange = (event) => {
    const { name, value, checked, type } = event.target;
    const newValue = type === 'checkbox' ? checked : value;
    setFormData({
      ...formData,
      [name]: newValue,
    });
  };
  useEffect(() => {
    clients 
      .get("/api/user")
      .then(function (res) {
        setIsAuthenticated(true);
        clients .get("/api/user/profile/")
          .then(function (res) {
            const userProfile = res.data.user;
            setFormData(userProfile);
          })
          .catch(function (error) {
            setIsEditing(isEditing)
          });
      })
      .catch(function (error) {
       

      });

  
  }, [isAuthenticated])
  
  
  const handleSubmit = async (e) => {
    e.preventDefault();
    clients 
      .get("/api/user")
      .then(function (res) {
        setIsAuthenticated(true);
        
      })
      .catch(function (error) {
        // Redirect to the login page if there's no currentUser
        navigate('/login');

      });

      // Send updated profile data to the server
      clients .post("/api/user/profile/", formData)
          .then(function (res) {
              setIsEditing(!isEditing)
          })
          .catch(function (error) {
          });
    
  };

  const toggleEditing = () => {
    setIsEditing(!isEditing);
};
  return (
    <>
      <Typography variant="h6" gutterBottom>
        Shipping address
      </Typography>
      {isEditing ? (
        
        <>
        <Grid container spacing={3}>
        <Grid item xs={12} sm={6}>
            <TextField
              required
              id="full_name"
              name="full_name"
              label="Full name"
              fullWidth
              autoComplete="given-name"
              variant="standard"
              value={formData.full_name}
              onChange={handleChange}
            />
          </Grid>
        
          <Grid item xs={12}>
            <TextField
              required
              id="phone"
              name="phone"
              label="Phone"
              fullWidth
              autoComplete="tel"
              variant="standard"
              value={formData.phone}
              onChange={handleChange}
            />
          </Grid>
          <Grid item xs={12}>
            <TextField
              required
              id="address"
              name="address"
              label="Address"
              fullWidth
              autoComplete="address"
              variant="standard"
              value={formData.address}
              onChange={handleChange}
            />
          </Grid>
         
         
         
          <Grid item xs={12}>
            <FormControlLabel
              control={
                <Checkbox
                  color="secondary"
                  name="saveAddress"
                  checked={formData.saveAddress}
                  onChange={handleChange}
                />
              }
              label="Use this address for payment details"
            />
          </Grid>
        </Grid>
        <Button
          variant="contained"
          color="primary"
          onClick={handleSubmit}
        >
          Save Address
        </Button>
        </>
      ) : (
        <div>


        <div className="band    p-4 rounded-md shadow-md mt-2 font-semibold text-md">
          <div className='flex justify-between w-18'>
            <div className="p-2">
              <p>
                Full Name:<span>&nbsp;&nbsp;{formData.full_name}</span>
              </p>
              <p>
                Phone:<span>&nbsp;&nbsp;{formData.phone}</span>
              </p>
              <p>
                Address:<span>&nbsp;&nbsp;{formData.address}</span>
              </p>
            </div>
            <div className="eadit p-4" style={{ cursor: 'pointer' }} onClick={toggleEditing}>
              <EditLocationAltTwoToneIcon />
            </div>
          </div>
        </div>

      </div>
        
      )}
    </>

  );
}
