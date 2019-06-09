import * as React from 'react';
import olMap from 'ol/Map'

import olStyle from 'ol/style/Style';
import olFillStyle from 'ol/style/Fill';
import olStrokeStyle from 'ol/style/Stroke';

// import {olFill, olStroke, olStyle} from 'ol/style.js';

import { List, Button, Modal, Spin } from 'antd';
import LayerListItem from './LayerListItem';

import axios from 'axios';
// import './style.scss'

const BStyle = new olStyle({
  fill: new olFillStyle({ color: [45, 189, 189, 0] }),
  stroke: new olStrokeStyle({
    color: '#2dbdbd',
    width: 1,
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


interface Props {
  map: olMap;
}
interface State {
  pending: boolean;
}

export class LayerList extends React.PureComponent<Props> {
  state: State = { pending: false }
  data = [
    { title: 'НТО', url: 'api/ntopoly/', style: GStyle },
    { title: 'Постройки', url: 'api/advertising/', style: RStyle },
    { title: 'Зеленые насаждения', url: 'api/green/', style: NStyle },
    { title: 'Рекламные конструкции', url: 'api/buildings/', style: BStyle },
    { title: 'Муниципальное дошкольное учеждения', },
    { title: 'Судебные участки мировых судей', },
    { title: 'Детские игровые площадки', },
  ]

  sychData = async () => {
    try {
      this.setState({ pending: true });
      await axios.get('/parser')
    } catch{
      Modal.error({ title: 'Ошибка при синхронизации объектов' })
    }
    finally {
      this.setState({ pending: false });
    }
  }

  render() {

    let { map } = this.props;
    let { pending } = this.state;
    let { sychData } = this;

    return (
      <div className="layer-list" >
        <Spin spinning={pending}>
          <List
            style={{ marginTop: 80, marginRight: 100 }}
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
          <Button onClick={sychData}> Синхронизировать </Button>
        </Spin>
      </div >
    )
  }
}