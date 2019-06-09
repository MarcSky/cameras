import * as React from 'react'
import * as ReactDOM from 'react-dom'

import axios from 'axios'

import { LayerList, CamSettings, Map } from '../components';

import olMap from 'ol/Map.js';
import olView from 'ol/View.js';
import olTileLayer from 'ol/layer/Tile'
import olXYZ from 'ol/source/XYZ';
import OSM from 'ol/source/OSM.js';

import { Button } from 'antd'

interface State {
  map?: olMap;
  mod: 'list' | 'cams'
}

export class LayOut extends React.Component<{}, State> {
  state: State = {mod: 'list'}
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
    let {map, mod} = this.state;
    return (
      <div className="content">
        <Button
          size="large"
          style={{ display: 'absolute', top: 30, left: 1150, zIndex: 1000 }}
          icon="unordered-list"
          shape="circle"
          onClick={() => this.setState({mod: 'list'})}/>
        <Button
          size="large"
          style={{ display: 'absolute', top: 30, left: 1200, zIndex: 1000 }}
          icon="video-camera"
          shape="circle"
          onClick={() => this.setState({mod: 'cams'})}/>
        {
          map !== undefined && (
            mod === 'list' && (
              <div className="left-content">
                <LayerList map={map} />
              </div>) ||
            mod === 'cams' && (
              <div className="left-content">
                <CamSettings map={map}/>
              </div>
              )
          )

        }
          <div className="right-content">
            <Map />
          </div>
      </div>
    )

  }
}
