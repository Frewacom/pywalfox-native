# Copy native app manifest to path read by Firefox
NHPATH="${HOME}/.mozilla/native-messaging-hosts"
MANIFEST_PATH="$NHPATH/pywalfox.json"
CURRENTPATH=$(pwd)
EXECUTABLE_NAME="daemon.py"

if [ ! -f "./$EXECUTABLE_NAME" ]; then
  echo "Could not find path to daemon. Are you in the root folder of Pywalfox?"
  exit
fi

if [ $(id -u) -eq 0 ]; then
  echo "Do not run this script using sudo."
  exit
fi

echo "Creating 'native-messaging-hosts' folder in ~/.mozilla"
mkdir -p $NHPATH

if [ -f "$MANIFEST_PATH" ]; then
  rm $MANIFEST_PATH
fi

echo "Copying native messaging manifest to $MANIFEST_PATH"
cp ./daemon/assets/pywalfox-manifest.json $MANIFEST_PATH

echo "Setting path to $EXECUTABLE_NAME in the manifest"
sed -i "s+<path>+$CURRENTPATH/$EXECUTABLE_NAME+g" $MANIFEST_PATH

echo "Setting execution permissions on $EXECUTABLE_NAME"
chmod +x ./$EXECUTABLE_NAME

echo "Finished."
