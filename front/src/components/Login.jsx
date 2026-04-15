import { useNavigate, Link } from 'react-router-dom';
import { mockApi } from '../services/mockApi';

export default function Login() {
  const navigate = useNavigate();

  function handleLogin(e) {
    e.preventDefault();
    mockApi.setSession({ loggedIn: true });
    navigate('/', { replace: true });
  }

  return (
    <div className="login-page">
      <div className="login-blob login-blob--1" aria-hidden />
      <div className="login-blob login-blob--2" aria-hidden />
      <div className="login-blob login-blob--3" aria-hidden />
      <div className="login-card">
        <h1>Вход</h1>
        <p className="sub">Войдите или зарегистрируйтесь</p>
        <form onSubmit={handleLogin}>
          <div className="login-field">
            <span className="ico" aria-hidden>
              👤
            </span>
            <input
              name="user"
              placeholder="Имя пользователя/электронная почта"
              autoComplete="username"
            />
          </div>
          <div className="login-field">
            <span className="ico" aria-hidden>
              🔒
            </span>
            <input
              type="password"
              name="pass"
              placeholder="Пароль"
              autoComplete="current-password"
            />
          </div>
          <div className="forgot">
            <a href="#forgot" onClick={(e) => e.preventDefault()}>
              Забыли пароль?
            </a>
          </div>
          <div className="login-actions">
            <button type="submit" className="btn btn--primary">
              Вход
            </button>
          </div>
        </form>
        <div className="footer-link">
          <Link to="/register">Регистрация</Link>
        </div>
      </div>
    </div>
  );
}
