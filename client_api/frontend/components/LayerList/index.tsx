import * as React from 'react';
import olMap from 'ol/Map'

import olStyle from 'ol/style/Style';
import olFillStyle from 'ol/style/Fill';
import olStrokeStyle from 'ol/style/Stroke';

// import {olFill, olStroke, olStyle} from 'ol/style.js';

import { List, Button } from 'antd';
import LayerListItem from './LayerListItem';

// import './style.scss'

interface Props {
  map: olMap;
}

const BStyle = new olStyle({
  fill: new olFillStyle({ color: [0, 0, 0, 0] }),
  stroke: new olStrokeStyle({
    color: '#000000',
    width: 3,
  }),
});


const GStyle = new olStyle({
  fill: new olFillStyle({ color: [0, 255, 0, 0] }),
  stroke: new olStrokeStyle({
    color: '#00ff00',
    width: 3,
  }),
});

const NStyle = new olStyle({
  fill: new olFillStyle({ color: [255, 0, 255, 0] }),
  stroke: new olStrokeStyle({
    color: '#ff0000',
    width: 3,
  }),
});

const RStyle = new olStyle({
  fill: new olFillStyle({ color: [255, 255, 0, 0] }),
  stroke: new olStrokeStyle({
    color: '#000000',
    width: 3,
  }),
});


export class LayerList extends React.PureComponent<Props> {

  data = [
    { title: 'Зеленые насаждения', url: 'api/ntopoly/', style: GStyle },
    { title: 'Постройки', url: 'api/advertising/', style: BStyle },
    { title: 'НТО', url: 'api/green/', style: NStyle },
    { title: 'Рекламные конструкции', url: 'api/buildings/', style: RStyle },
  ]

  render() {

    let { map } = this.props;
    return (
      <div className="layer-list" >
        <List
          style={{margin: 30}}
          header="Список доступных слоев"
          dataSource={this.data}
          renderItem={item =>
            <LayerListItem
              map={map}
              title={item.title}
              url={item.url}
              style={item.style}
            />
          }
        />
        <Button> 123 </Button>
      </div >
    )
  }
}