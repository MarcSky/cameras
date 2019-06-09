import React from 'react';
import olMap from 'ol/map';
import olDrawInteraction from 'ol/interaction/Draw.js';

import olVectorLayer from 'ol/layer/Vector';
import olVectorSource from 'ol/source/Vector';

import olPolygonGeom from 'ol/geom/Polygon';
import GeoJSON from 'ol/format/GeoJSON.js';

import { List, Button, Modal, Spin, Icon, Form, InputNumber, Menu, Switch } from 'antd';
import LayerListItem from './LayerListItem';


import olStyle from 'ol/style/Style';
import olFillStyle from 'ol/style/Fill';
import olStrokeStyle from 'ol/style/Stroke';

import axios from 'axios';
// import './style.scss'f

interface Props {
  map: olMap;
}

interface State {
  pending: boolean;
  countCam: number;
  polygon?: olPolygonGeom;
}

export class CamSettings extends React.PureComponent<Props> {
  state: State = { pending: false, countCam:0}
  
  drawInter?:olDrawInteraction;
  dravLayer?:olVectorLayer;
  camLayer?: olVEctorLayer;

  const data = [
	  <List.Item key="1" style={{display: 'flex', justifyContent: 'space-between'}}>
	  	<span> Число камер </span> 
	  	<span> 
		  	<InputNumber 
		  		min={0} 
		  		defaultValue={this.state.countCam}
		  		onChange={(value)=>this.setState({countCam: value})}
		  	/> 
	  	</span>
    </List.Item>,
	  <List.Item key="2" style={{display: 'flex', justifyContent: 'space-between'}}>
	  	<Menu  mode="inline" > 
 				<Menu.SubMenu key="sub3" title="Выбрать границы">
          <Menu.Item key="3"
          	onClick={() => this.updateInteracion(false)}>Из списка</Menu.Item>
          <Menu.Item 
          	style={{color: '#555599'}} 
          	key="4" 
          	onClick={() => this.updateInteracion(true)}
          >На карте</Menu.Item>
        </Menu.SubMenu>
	  	</Menu>
    </List.Item>,
    <List.Item key="5" style={{display: 'flex', justifyContent: 'space-between'}}>
	  	<span> Привязка к слоям </span> <span> <Switch/> </span>
    </List.Item>,
    <List.Item key="6" style={{display: 'flex', justifyContent: 'space-between'}}>
	  	<Button block type="primary" onClick={() => 
	  		this.fetchCam()
	  	}> Расчет </Button>
    </List.Item>,
    <List 
    	header="Архив расчетов"
    />

	];

	fetchCam = async () => {
		let {countCam} = this.state;
		let {map} = this.props;

		this.setState({pending: true});
		try{
			let response = await axios.get(`api/res-point2/`);
			let results = response.data.features;

			if (results.length){
        var vectorSource = new olVectorSource({
          features: new GeoJSON().readFeatures({
            type: 'FeatureCollection',
            features: results
          })
        });

        const RStyle = new olStyle({
				  fill: new olFillStyle({ color: [206, 255, 0, 70] }),
				  stroke: new olStrokeStyle({
				    color: '#ceae7f',
				    width: 1,
				  }),
				});

        let layer = new olVectorLayer({
          source: vectorSource,
          name: 'cam',
          opacity: 0.7,
          style: RStyle,
        });

        // this.setState({ layer });

        let thisLayers = map.getLayers().getArray();
        let camLayer = thisLayers.find((item) => item.get('name') === 'cam');
        if (camLayer !== undefined){
        	map.removeLayer(camLayer)
        }
        map.addLayer(layer);
				// this.camLayer.setMap(map);
			}
		}
		catch(err){
			console.log(err)
			Modal.error({title: 'Ошибка при загрузке камер'});
		}finally{
			this.setState({pending: false})
		}
	}

	componentDidMount(){
		let source = new olVectorSource();
		
		this.dravLayer = new olVectorLayer({source: source});
		this.drawInter = new olDrawInteraction({
	  	source: source,
	  	type: 'Polygon',
	  });
	}

	updateInteracion = (isIter) => {
		if (!isIter){
			this.props.map.removeInteraction(this.drawInter);
			this.dravLayer.setMap(null);
		}else{
			this.props.map.addInteraction(this.drawInter);
			this.dravLayer.setMap(this.props.map);
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
            header="Расчет камер"
            dataSource={this.data}
            renderItem={item =>  item}
          />
        </Spin>
      </div >
    )
  }
}