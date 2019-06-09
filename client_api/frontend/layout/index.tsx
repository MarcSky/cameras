import * as React from 'react'
import * as ReactDOM from 'react-dom'

import axios from 'axios'

import { LayerList, Map } from '../components';

import olMap from 'ol/Map.js';
import olView from 'ol/View.js';
import olTileLayer from 'ol/layer/Tile'
import olXYZ from 'ol/source/XYZ';
import OSM from 'ol/source/OSM.js';


interface State {
  map?: olMap;
}

export class LayOut extends React.Component<{}, State> {
  state: State = {}
  componentDidMount() {
    let map = new olMap({
      target: 'map',
      layers: [
        new olTileLayer({
          source: new OSM()
        })
      ],
      view: new olView({
        projection: 'EPSG:4326',
        center: [39.72, 47.23],
        zoom: 16
      })
    });

    this.setState({ map })
  }

  render() {
    return (
      <div className="content">
        {
          this.state.map !== undefined && (
            <>
              <div className="left-content">
                <LayerList map={this.state.map} />
              </div>
            </>
          )
        }

        <div className="right-content">
          <Map />
        </div>
      </div>
    )

  }
}
