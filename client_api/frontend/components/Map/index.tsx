import * as React from 'react'

import olMap from 'ol/Map.js';
import olView from 'ol/View.js';
import olTileLayer from 'ol/layer/Tile'
import olXYZ from 'ol/source/XYZ';

export class Map extends React.PureComponent {
  render() {
    return (
      <div className="map" id="map"></div>
    )
  }
}