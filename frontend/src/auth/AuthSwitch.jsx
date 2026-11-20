export default function AuthSwitch({
  isRegister,
  disabled,
  onRegister,
  onLogin,
}) {
  return (
    <div className="auth-switch" role="group" aria-label="Wybór formularza">
      <button
        type="button"
        aria-pressed={!isRegister}
        disabled={disabled}
        onClick={onLogin}
      >
        Zaloguj się
      </button>

      <button
        type="button"
        aria-pressed={isRegister}
        disabled={disabled}
        onClick={onRegister}
      >
        Załóż konto
      </button>
    </div>
  )
}