
import Avatar from '@mui/material/Avatar';
import Button from '@mui/material/Button';
import CssBaseline from '@mui/material/CssBaseline';
import TextField from '@mui/material/TextField';
import FormControlLabel from '@mui/material/FormControlLabel';
import Checkbox from '@mui/material/Checkbox';
import Link from '@mui/material/Link';
import Paper from '@mui/material/Paper';
import Box from '@mui/material/Box';
import Grid from '@mui/material/Grid';
import LockOutlinedIcon from '@mui/icons-material/LockOutlined';
import Typography from '@mui/material/Typography';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import React, { useEffect, useState } from 'react'
import clients  from '../../components/api/Client'
import { useNavigate } from 'react-router-dom';
import Snackbar from '@material-ui/core/Snackbar';
import MuiAlert from '@material-ui/lab/Alert';
import LoadingBar from 'react-top-loading-bar'


// TODO remove, this demo shouldn't need to reset the theme.
const defaultTheme = createTheme();

export default function Login() {
  const [progress, setProgress] = useState(0)
  const [currentUser, setCurrentUser] = useState();
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [formData, setFormData] = useState({
    username: '',
    password: '',
  });
  const [openSnackbar, setOpenSnackbar] = useState(false);

  const handleSnackbarClose = (event, reason) => {
    if (reason === 'clickaway') {
      return;
    }
    setOpenSnackbar(false);
  };
  const navigate = useNavigate();
  function submitLogin(e) {
    setProgress(10);
    e.preventDefault();
    clients.post(
      "/api/login/",
      {
        username: username,
        password: password
      }
    ).then(function (res) {
      setProgress(50);
      setCurrentUser(true);
      navigate('/myaccount');
      window.location.reload();
      setProgress(100);
    })
    .catch(function (error) {
      setProgress(50);
      setCurrentUser(false);
      setOpenSnackbar(true);
      setProgress(100);
        // Redirect to the login page if there's no currentUser

      });
  }
  useEffect(() => {
    setProgress(10);
    clients
    .get("/api/user")
    .then(function (res) {
      setProgress(60);
      navigate('/myaccount'); // Change '/login' to the actual login page URL
      setCurrentUser(true);
      window.location.reload();
      setProgress(100);
    })
    .catch(function (error) {
      setProgress(60);
      setCurrentUser(false);
      setProgress(100);
        // Redirect to the login page if there's no currentUser

      });
  }, [currentUser, navigate]);

useEffect(() => {
  // Remove all non-digit characters from the username
  const value = username.replace(/\D/g, '');

  // Update the formData state with the sanitized username
  setFormData({ ...formData, username: value });
}, [username]);
return (
    <div >
       <LoadingBar
        color='#f11946'
        progress={progress}
        onLoaderFinished={() => setProgress(0)}
      /> 
      <Snackbar open={openSnackbar} autoHideDuration={6000} onClose={handleSnackbarClose}>
            <MuiAlert elevation={6} variant="filled" onClose={handleSnackbarClose} severity="warning">
              Check Phone Number & Password
            </MuiAlert>
          </Snackbar>
      
      <div className='flex justify-center mt-10 mb-20 p-4'>
        
          <div className='flex flex-col justify-items-center '
           
          >
            <div className='theme_color flex justify-center m-auto rounded-full w-10 h-10'>
              <LockOutlinedIcon className='self-center text-white' />
            </div>
            <div className='text-xl text-center font-semibold'>
              Sign in
            </div>
            
            <Box component="form" noValidate onSubmit={e => submitLogin(e)}sx={{ mt: 1 }}>
              <TextField
                margin="normal"
                required
                fullWidth
                id="username"
                label="Phone Number"
                name="username"
                autoComplete="tel"
                autoFocus
                value={username}
                onChange={(e) => {
                  const input = e.target.value;
                  // Use a regular expression to remove all non-numeric characters
                  const numericInput = input.replace(/\D/g, '');
                  // Update the state with the numeric input
                  setUsername(numericInput);
                }}
              />


              <TextField
                margin="normal"
                required
                fullWidth
                name="password"
                label="Password"
                type="password"
                id="password"
                value={password} onChange={e => setPassword(e.target.value)}
                autoComplete="current-password"
              />
             
              <button 
                className='theme_color theme_colol w-full text-center p-2 mt-4 mb-4 text-white font-semibold text-xl rounded-full shadow-md dark:shadow-gray-200'
              >
                Sign In
              </button>
              <Grid container>
                <Grid item xs>
                  <Link href="#" variant="body2">
                    Forgot password?
                  </Link>
                </Grid>
                <Grid item>
                  <Link href="/register" variant="body2">
                    <a>
                    </a>
                    {"Don't have an account? Sign Up"}
                  </Link>
                </Grid>
              </Grid>
            </Box>
          </div>
       
      </div>
    </div>
);
}