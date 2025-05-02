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
import { useState, useEffect} from 'react'; // Import useState

const App = () => {
  // Define state for medicines in the App component
  const [medicines, setMedicines] = useState([]); // Step 1: Define medicines state
  useEffect(() => {
    let isMounted = true;
  
    const getPrescriptions = async () => {
      try {
        const data = await fetchPrescriptions();
        if (isMounted) {
          setMedicines(prevState => [...prevState, ...data]);
        }
      } catch (error) {
        if (isMounted) {
          console.error('Error fetching prescriptions:', error);
        }
      }
    };
  
    getPrescriptions();
  
    return () => {
      isMounted = false; // Cleanup to prevent state update
    };
  }, []);
  
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
        element: <PrescriptionTracker medicines={medicines} setMedicines={setMedicines}/>,
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
