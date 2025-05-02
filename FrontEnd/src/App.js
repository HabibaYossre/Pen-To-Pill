import './App.css';
import PrescriptionTracker from './Components/PrescriptionTracker';
import Home from './Components/Home';
import Layout from './Components/Layout';
import AddPrescription from './Components/AddPrescription';
import AboutUs from './Components/AboutUs';
import { fetchPrescriptions } from './dbOperations';
import {
  createHashRouter,
  RouterProvider,
} from "react-router-dom";
import { useState, useEffect } from 'react';

const App = () => {
  // Define state for medicines in the App component
  const [medicines, setMedicines] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  
  useEffect(() => {
    let isMounted = true;
    
    const getPrescriptions = async () => {
      setIsLoading(true);
      try {
        const data = await fetchPrescriptions();
        if (isMounted) {
          // Replace the state instead of appending
          setMedicines(data);
        }
      } catch (error) {
        if (isMounted) {
          console.error('Error fetching prescriptions:', error);
        }
      } finally {
        if (isMounted) {
          setIsLoading(false);
        }
      }
    };
    
    getPrescriptions();
    
    return () => {
      isMounted = false; // Cleanup to prevent state update
    };
  }, []); // Empty dependency array ensures this runs only once
  
  // Define your routes
  const routes = createHashRouter([{
    path: '/',
    element: <Layout />,
    children: [
      {
        path: "/",
        element: <Home />,
      },
      {
        path: "Add-Prescription",
        element: <AddPrescription setMedicines={setMedicines} />,
      },
      {
        path: "View-Schedule",
        element: 
          <PrescriptionTracker 
            medicines={medicines} 
            setMedicines={setMedicines}
            isLoading={isLoading}
          />,
      },
      {
        path: "About-us",
        element: <AboutUs />,
      },
    ],
  }]);
  
  return (
    <RouterProvider router={routes} />
  );
}

export default App;