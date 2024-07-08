import { createBrowserRouter } from "react-router-dom";

import App from "./components/App";
import Login from './components/Login';
import Map from './components/Map';
import Register from './components/Register';
import PlaceList from './components/PlaceList';
import CreatePlace from './components/CreatePlace';
import PlaceDetails from './components/PlaceDetails';
import CreateRoute from './components/CreateRoute';
import OurCommunity from './components/OurCommunity';
import Profile from './components/Profile';
import RouteList from "./components/RouteList";
import RouteDetails from "./components/RouteDetail";

const routes = [
    {
      path: '/',
      element: <App />,
      children: [
        { index: true, element: <Profile /> },
        { path: '/login', element: <Login /> },
        { path: '/map', element: <Map /> },
        { path: '/register', element: <Register /> },
        { path: '/places', element: <PlaceList /> },
        { path: '/places/new', element: <CreatePlace /> },
        { path: '/places/:placeId', element: <PlaceDetails /> },
        { path: '/routes', element: <RouteList /> },
        { path: '/routes/new', element: <CreateRoute /> },
        { path: '/routes/:routeId', element: <RouteDetails /> },
        { path: '/community', element: <OurCommunity /> },
        { path: '/profile', element: <Profile /> }
      ]
    }
  ];
  
export const router = createBrowserRouter(routes)