import * as React from 'react';
import olMap from 'ol/Map'
import olVectorLayer from 'ol/layer/Vector';
import olVectorSource from 'ol/source/Vector';

import olLayerGroup from 'ol/layer/Group'
import GeoJSON from 'ol/format/GeoJSON.js';

import olStyle from 'ol/style/Style';

import { Modal, Checkbox } from 'antd';
import axios from 'axios';


interface Props {
  title: string;
  url: string;
  map: olMap;
  style: olStyle;
}

interface State {
  visible: boolean;
  layer?: olVectorLayer;
}

// const headers = {
//   'Access-Control-Allow-Origin': '*',
//   'Content-Type': 'application/json',
//   'Origin': '*',
// }

export default class LayerListItem extends React.PureComponent<Props, State>{

  state: State = { visible: true }

  fetchLayers = async () => {
    let { url, title, map, style } = this.props;

    let thisLayers = map.getLayers().getArray()
    let thisLayer = thisLayers.find(layer => layer.get('name') === title)

    if (thisLayer === undefined) {
      try {
        let response = await axios.get(url)
        // let response = await axios.get(url, {
        //   method: 'GET',
        //   headers: {
        //     'Access-Control-Allow-Origin': '*',
        //     'Content-Type': 'application/json',
        //   },
        //   withCredentials: true,
        // })layer

        let results = response.data.features;

        if (results.length) {

          var vectorSource = new olVectorSource({
            features: new GeoJSON().readFeatures({
              type: 'FeatureCollection',
              features: results
            })
          });

          let layer = new olVectorLayer({
            source: vectorSource,
            style: style,
          });

          this.setState({ layer });
          map.addLayer(layer);
          // map.renderSync();
        }
      } catch (err) {
        console.log(err);
        // Modal.error({ title: `Ошибка при загрузки данных слоя ${title}` })
      }
    }
  }

  componentDidMount() {
    this.fetchLayers();
  }

  render() {
    let { title } = this.props;
    let { visible, layer } = this.state;

    return (
      <div className="list-item">
        {title}
        {
          layer !== undefined &&
          <Checkbox defaultChecked={visible} value={visible} onChange={() => {
            layer.setVisible(!visible);
            this.setState({ visible: !visible })
          }} />
        }
      </div>
    )
  }
}