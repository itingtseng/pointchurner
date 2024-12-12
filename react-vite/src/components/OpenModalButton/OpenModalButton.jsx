import { useModal } from '../../context/Modal';

function OpenModalButton({
  modalComponent, // Component to render inside the modal
  buttonText, // Text or content of the button that opens the modal
  onButtonClick, // Optional: Callback function for the button click
  onModalClose, // Optional: Callback function for when the modal closes
  className, // Optional: Additional class names for styling
  as // Optional: Component type to render (e.g., "button", "div", "span")
}) {
  const { setModalContent, setOnModalClose } = useModal();

  const onClick = (e) => {
    e.stopPropagation(); // Prevent unwanted bubbling
    if (onModalClose) setOnModalClose(onModalClose);
    setModalContent(modalComponent);
    if (typeof onButtonClick === "function") onButtonClick();
  };

  const Component = as || "button"; // Default to a <button> element if "as" is not provided

  return (
    <Component onClick={onClick} className={className}>
      {buttonText}
    </Component>
  );
}

export default OpenModalButton;
