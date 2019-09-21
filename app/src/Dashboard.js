import React, { Component } from "react";
 import { Map, GoogleApiWrapper } from 'google-maps-react';

 const mapStyles = {
  width: '60%',
  height: '50%',
};

class Dashboard extends Component {
  render() {
    return (
      <div className="content">
        <h2>Dashboard</h2>
        <p><Map
        google={this.props.google}
        zoom={5}
        style={mapStyles}
        initialCenter={{ lat: 25.2744, lng: 133.7751}}
      />
      </p>
      </div>
    );
  }
}
 
export default GoogleApiWrapper({
  apiKey: 'AIzaSyDZYctKuYZboWQRBWXdpAg0ga5UQZ4gw08'
})(Dashboard);
