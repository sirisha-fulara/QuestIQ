const avatars = [
  "/avatars/avatar1.png",
  "/avatars/avatar2.png",
  "/avatars/avatar3.png",
  "/avatars/avatar4.png",
  "/avatars/avatar5.png",
]

const AvatarSelector = ({ selected, onSelect }) => {
  return (
    <div className="avatar-selector">
      {avatars.map((img, i) => (
        <img
          key={i}
          src={img}
          alt="avatar"
          className={selected === img ? "active" : ""}
          onClick={() => onSelect(img)}
        />
      ))}
    </div>
  )
}

export default AvatarSelector