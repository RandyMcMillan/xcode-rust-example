set -euo pipefail

MY_CRATE=rustylib
SWIFT_APP=swiftyapp
SWIFT_PROJECT=swiftyrustlib
SWIFT_PROJECT_NAME=RustyLib
SWIFT_CORE_NAME=RustyCore

cd $MY_CRATE

# step 1 - compile rust library and generate bindings
HEADERPATH="out/${MY_CRATE}FFI.h"
TARGETDIR="$(cargo metadata --no-deps --format-version 1 | tr -d '\n' | sed -n 's/.*"target_directory":"\([^"]*\)".*/\1/p')"
TARGETDIR="${TARGETDIR:-target}"
OUTDIR="../${MY_CRATE}"
RELDIR="release"
STATIC_LIB_NAME="lib${MY_CRATE}.a"
NEW_HEADER_DIR="out/include"

DEVICE_TARGET="aarch64-apple-ios"

case "$(uname -m)" in
    arm64)
        SIMULATOR_TARGET="aarch64-apple-ios-sim"
        CATALYST_TARGET="aarch64-apple-ios-macabi"
        ;;
    x86_64)
        SIMULATOR_TARGET="x86_64-apple-ios"
        CATALYST_TARGET="x86_64-apple-ios-macabi"
        ;;
    *)
        echo "Unsupported host architecture: $(uname -m)" >&2
        exit 1
        ;;
esac

targets=("${DEVICE_TARGET}" "${SIMULATOR_TARGET}" "${CATALYST_TARGET}")

for target in "${targets[@]}"; do
    rustup target add ${target}
            cargo build --target "${target}" --release -j8
            cargo run --bin uniffi-bindgen generate --library "${TARGETDIR}/${target}/${RELDIR}/${STATIC_LIB_NAME}" --language swift --out-dir out
        done
# step 2 - create xcframework
mkdir -p "${NEW_HEADER_DIR}"
cp "${HEADERPATH}" "${NEW_HEADER_DIR}/"
cp "out/${MY_CRATE}FFI.modulemap" "${NEW_HEADER_DIR}/module.modulemap"

rm -rf "${OUTDIR}/${MY_CRATE}_framework.xcframework"

xcodebuild -create-xcframework \
    -library "${TARGETDIR}/${DEVICE_TARGET}/${RELDIR}/${STATIC_LIB_NAME}" -headers "${NEW_HEADER_DIR}" \
    -library "${TARGETDIR}/${SIMULATOR_TARGET}/${RELDIR}/${STATIC_LIB_NAME}" -headers "${NEW_HEADER_DIR}" \
    -library "${TARGETDIR}/${CATALYST_TARGET}/${RELDIR}/${STATIC_LIB_NAME}" -headers "${NEW_HEADER_DIR}" \
    -output "${OUTDIR}/${MY_CRATE}_framework.xcframework"

rm -rf "${NEW_HEADER_DIR}"

cd ../

SWIFT_LIB_PATH="./${SWIFT_APP}/Lib/${SWIFT_PROJECT}"

# step 3 - move to SwiftLib artifacts
if [ -d "${SWIFT_LIB_PATH}/artifacts" ]; then
    rm -rf "${SWIFT_LIB_PATH}/artifacts"
fi
mkdir "${SWIFT_LIB_PATH}/artifacts"
cp -R "./${MY_CRATE}/${MY_CRATE}_framework.xcframework" "${SWIFT_LIB_PATH}/artifacts"
mv "${SWIFT_LIB_PATH}/artifacts/${MY_CRATE}_framework.xcframework" "${SWIFT_LIB_PATH}/artifacts/${SWIFT_CORE_NAME}.xcframework"

# step 4 - move to SwiftLib Sources
if [ -d "${SWIFT_LIB_PATH}/Sources" ]; then
    rm -rf "${SWIFT_LIB_PATH}/Sources"
fi
mkdir "${SWIFT_LIB_PATH}/Sources"
mkdir "${SWIFT_LIB_PATH}/Sources/${SWIFT_PROJECT_NAME}"
cp "./${MY_CRATE}/out/${MY_CRATE}.swift" "${SWIFT_LIB_PATH}/Sources/${SWIFT_PROJECT_NAME}/${SWIFT_PROJECT_NAME}.swift"
