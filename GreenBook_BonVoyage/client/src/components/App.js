import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import Header from './Header';
import Home from './Home';
import Login from './Login';
import Map from './Map';
import Register from './Register';
import PlaceList from './PlaceList';
import CreatePlace from './CreatePlace';
import PlaceDetails from './PlaceDetails';
import CreateRoute from './CreateRoute';
import Chat from './Chat';
import Profile from './Profile';

const App = () => {
  return (
    <Router>
      <div className="app">
        <Header />
        <Switch>
          {/* Ensure each Route path matches correctly */}
          <Route exact path="/" component={Home } />
          <Route path="/login" component={Login } />
          <Route path="/map" component={Map } />
          <Route path="/register" component={Register} />
          <Route exact path="/places" component={PlaceList } />
          <Route path="/places/new" component={CreatePlace } />
          <Route path="/places/:placeId" component={PlaceDetails} />
          <Route path="/routes/new" component={CreateRoute } />
          <Route path="/chat" component={Chat } />
          <Route path="/profile" component={Profile } />
        </Switch>
      </div>
    </Router>
  );
};

export default App;
