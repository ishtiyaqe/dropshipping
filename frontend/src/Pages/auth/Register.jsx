
import { useState, useEffect } from 'react';
import Avatar from '@mui/material/Avatar';
import Button from '@mui/material/Button';
import CssBaseline from '@mui/material/CssBaseline';
import TextField from '@mui/material/TextField';
import Link from '@mui/material/Link';
import Grid from '@mui/material/Grid';
import Box from '@mui/material/Box';
import LockOutlinedIcon from '@mui/icons-material/LockOutlined';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import clients from '../../components/api/Client';
import Snackbar from '@material-ui/core/Snackbar';
import MuiAlert from '@material-ui/lab/Alert';
import LoadingBar from 'react-top-loading-bar'



function Register() {
  const [progress, setProgress] = useState(0)
  const [currentUser, setCurrentUser] = useState();
  const [username, setUsername] = useState('');
  const [ErrorMsg, setErrorMsg] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();
  const [openSnackbar, setOpenSnackbar] = useState(false);
  const handleSnackbarClose = (event, reason) => {
    if (reason === 'clickaway') {
      return;
    }
    setOpenSnackbar(false);
  };
  useEffect(() => {
    setProgress(10);
    clients
      .get("/api/user/")
      .then(function (res) {
        setProgress(50);
        navigate('/myaccount');; // Change '/login' to the actual login page URL
        setCurrentUser(true);
        window.location.reload();
        setProgress(100);
      })
      .catch(function (error) {
        setProgress(50);
        setCurrentUser(false);

        
        // Redirect to the login page if there's no currentUser
        if (!currentUser) {
          navigate('/register/');; // Change '/login' to the actual login page URL
          setProgress(100);
        }
      });
  }, []);
  function submitRegistration(e) {
    setProgress(10);
    e.preventDefault();
    clients.post(
      "http://192.168.0.105:8000/api/register/",
      {
        "username": username,
        "password": password
      }
    ).then(function (res) {
      setProgress(50);
      clients.post(
        "/api/login/",
        {
          "username": username,
          "password": password
        }
      ).then(function (res) {
        setCurrentUser(true);
        navigate('/myaccount');
        setProgress(100);
      })
        .catch(function (error) {
          setProgress(50);
          setOpenSnackbar(true);
          setErrorMsg(error)
          setProgress(50);
          setCurrentUser(false);
          
          // Redirect to the login page if there's no currentUser
          setProgress(100);


        });

    }) .catch(function (error) {
      setProgress(50);
      setOpenSnackbar(true);
      setErrorMsg(error.response.data.username)
      
      setProgress(50);
      setCurrentUser(false);
      
      // Redirect to the login page if there's no currentUser
      setProgress(100);


    })
  }



  return (
    <ThemeProvider theme={createTheme()}>
      <Snackbar open={openSnackbar} autoHideDuration={6000} onClose={handleSnackbarClose}>
        <MuiAlert elevation={6} variant="filled" onClose={handleSnackbarClose} severity="warning">
          {ErrorMsg}
        </MuiAlert>
      </Snackbar>
      <LoadingBar
        color='#f11946'
        progress={progress}
        onLoaderFinished={() => setProgress(0)}
      />
      <Container component="main" maxWidth="xs">
        <CssBaseline />
        <Box
          sx={{
            marginTop: 8,
            marginBottom: 10,
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
          }}
        >
          <Avatar sx={{ m: 1, bgcolor: 'secondary.main' }}>
            <LockOutlinedIcon />
          </Avatar>
          <Typography component="h1" variant="h5">
            Sign up
          </Typography>
          <Box component="form" noValidate onSubmit={e => submitRegistration(e)} sx={{ mt: 3 }}>
            <div className='space-y-2'>

              <TextField
                required
                fullWidth
                id="username"
                label="Phone Number"
                name="username"
                autoComplete="Phone Number"
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
                required
                fullWidth
                name="password"
                label="Password"
                type="password"
                id="password"
                autoComplete="new-password"
                value={password} onChange={e => setPassword(e.target.value)}
              />
            </div>
            <button
              className='theme_color theme_colorl w-full p-4 text-center shadow-md dark:shadow-gray-200 rounded-full mt-4 mb-4 font-semibold text-white'
            >
              Sign Up
            </button>
            <Grid container justifyContent="flex-end">
              <Grid item>
                <Link href="/login" variant="body2">
                  Already have an account? Sign in
                </Link>
              </Grid>
            </Grid>
          </Box>
        </Box>
      </Container>
    </ThemeProvider>
  );
}

export default Register;
