import { Container, Nav, Navbar, NavbarCollapse} from 'react-bootstrap';
import logo from '../../imgs/glavlog.png'
import userlogo from '../../imgs/Vector.png'
import {BrowserRouter as Router, Route, Routes} from 'react-router-dom';
import Home from '../../pages/Home/Home';
import Statistics from '../../pages/Statistics';
import Contacts from "../../pages/Contacts";
import Zayvka from '../../Zayvka';
import '../../App.css'

function Header() {
  return (
    <>
        <Navbar fixed='top' collapseOnSelect expand='md' style={{backgroundColor: '#2cb641', color:"#D0D0D0", height:'45px'}}>
          <Container >
            <Navbar.Brand href='/' style={{ display: 'flex', alignItems: 'center' }}>
              <img src={logo} height={40} width={40} alt='Logo'/>
              <span style={{ paddingLeft: '10px' }}>Защитник природы</span>
            </Navbar.Brand>
            <Navbar.Toggle aria-controls='responsive-navbar-nav'/>
            <NavbarCollapse id='responsive-navbar-nav' style={{flexDirection: 'row-reverse'}}>
              <Nav className='mr-auto'>
                <Nav.Link href='/'>Главная</Nav.Link>
                <Nav.Link href='/statistics'>Статистика</Nav.Link>
                <Nav.Link href='/contacts'>Контакты</Nav.Link>
                <Nav.Link href='/Zayvka'>Заявка</Nav.Link>
              </Nav>
            </NavbarCollapse>
            <Navbar.Brand href='/' >
              <img src={userlogo} height={30} width={30} alt='UserLogo' style={{ marginLeft: '15px' }}/>
            </Navbar.Brand>
          </Container>
        </Navbar>

        <Router>
          <Routes>
            <Route exact path='/' element={<Home />} />
            <Route exact path='/statistics' element={<Statistics />} />
            <Route exact path='/Zayvka' element={<Zayvka />} />
            <Route exact path='/Contacts' element={<Contacts />} />
          </Routes>
        </Router>
    </>
  )
}

export default Header;
