import './App.css';
import PrescriptionTracker from './Components/PrescriptionTracker';
import Home from './Components/Home';
import Layout from './Components/Layout';
import {
  createBrowserRouter,
  createHashRouter,
  RouterProvider,
} from "react-router-dom";

const routes = createBrowserRouter([{
  path: '',
  element: <Layout/>,
  children: [
    {
      path: "/",
      element: <Home />,
    },
    {
      path: "Add-Prescription",
      element: <PrescriptionTracker />,
    }
  ]
}]);

function App() {
  return <RouterProvider router={routes} />;
}

export default App;
