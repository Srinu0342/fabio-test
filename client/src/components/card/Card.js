export function Card({ title, link }) {
  return (
    <div>
      <p>{title}</p>
      <img src={link} alt={'Cats'}/>
    </div>
  );
}