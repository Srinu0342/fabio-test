import { useState, useMemo, useEffect } from 'react';
import './App.css';
import axios from 'axios';
import debounce from 'lodash.debounce';
import { Card } from './components/card/Card';
import Modal from "react-overlays/Modal";
const backendUrl = process.env.REACT_APP_BACKEND_URL;

function App() {
  const [cardList, setCardList] = useState();
  const [stableList, setStableList] = useState();
  const [bufferData, setBufferData] = useState();
  const [modalState, setModalState] = useState({ show: false, link: '' });
  const [loader, setLoader] = useState(false);
  const fetchRecordsURL = useMemo(() => `${backendUrl}/records`, []);
  // const updateRecordsURL = useMemo(() => `${backendUrl}/save/positions`, []);
  const bulkUpdateUrl = useMemo(() => `${backendUrl}/bulk-update`, []);
  const debouncedSetRecords = useMemo(() =>
    debounce((recordList, storedRecordList) => {
      setLoader(true)
      const snapshot = recordList.filter((item, index) => {
        const list = storedRecordList[index];
        const check = item.title !== list.title || item.type !== list.type || item.link !== list.link;
        return check;
      });
      axios.post(bulkUpdateUrl, {
        values: snapshot,
      }).then(() => {setLoader(false)})
    }, 5000), [bulkUpdateUrl]);

  const handleClose = () => setModalState({ show: false, link: '' });
  const onDragStart = (e, item, index) => {
    setBufferData({ item: item, index });
  }
  const allowDrop = (e) => {
    e.preventDefault();
  }
  const onDrop = (e, item, index) => {
    const cardListData = [...cardList];
    cardListData[index] = { ...bufferData.item, position: item.position };
    cardListData[bufferData.index] = { ...item, position: bufferData.item.position };
    // axios.post(updateRecordsURL, {
    //   values: {
    //     firstRecord: item,
    //     secondRecord: bufferData.item,
    //   },
    // })
    debouncedSetRecords(cardListData, stableList);
    setCardList(cardListData);
  }

  useEffect(() => {
    axios.post(fetchRecordsURL).then(data => {
      setStableList(data.data.values);
      setCardList(data.data.values);
    })
  }, [fetchRecordsURL]);

  const renderBackdrop = (props) => <div className="backdrop" {...props} />;

  return (
    <div className="App">
      <header className="App-header">
      {loader
        ?  <div className='loader-box'>
              <div className="loader"></div>
            </div>
        : <></>}
        <div style={
          {
            marginLeft: '15%',
            marginRight: '15%',
            display: 'flex',
            flexFlow: 'row wrap',
            justifyContent: 'center',
          }
        }>
          { cardList?.length ? 
            cardList.map((item, index) => {
              return (
                <div
                  draggable={true}
                  style={{ margin: '50px', cursor: 'pointer' }}
                  onDragStart={(e) => { onDragStart(e, item, index)}}
                  onDragOver={allowDrop}
                  onDrop={(e) => { onDrop(e, item, index) }}
                  onClick={() => setModalState({ show: true, link: item.link })}
                  key={item.position}
                >
                  <Card title={item.title} link={item.link}/>
                </div>
              );
            }) : <></>
          }
        </div>
        <Modal
          className="modal"
          show={modalState.show}
          onHide={handleClose}
          renderBackdrop={renderBackdrop}
        >
          <img src={modalState.link} alt={'cat'}/>
        </Modal>
      </header>
    </div>
  );
}

export default App;
