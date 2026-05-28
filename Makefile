SHELL := /bin/bash

PROJECT := swiftyapp/swiftyapp.xcodeproj
SCHEME := swiftyapp
BUILD_SCRIPT := ./build.sh
RUST_CRATE_DIR := rustylib
DERIVED_DATA ?= .build/xcode
IOS_DESTINATION ?= generic/platform=iOS Simulator
CATALYST_DESTINATION ?= generic/platform=macOS,variant=Mac Catalyst

.DEFAULT_GOAL := help

.PHONY: help rust resolve app catalyst clean

help:
	@printf '%s\n' \
		'make rust      - build the Rust library, bindings, and XCFramework' \
		'make resolve   - resolve local Swift package dependencies' \
		'make app       - build the iOS app for a generic simulator destination' \
		'make catalyst  - build the app for Mac Catalyst' \
		'make clean     - clean Rust and Xcode build artifacts'

rust:
	$(BUILD_SCRIPT)

resolve:
	xcodebuild -resolvePackageDependencies -project "$(PROJECT)" -scheme "$(SCHEME)"

app: rust resolve
	xcodebuild \
		-project "$(PROJECT)" \
		-scheme "$(SCHEME)" \
		-derivedDataPath "$(DERIVED_DATA)" \
		-destination "$(IOS_DESTINATION)" \
		build

catalyst: rust resolve
	xcodebuild \
		-project "$(PROJECT)" \
		-scheme "$(SCHEME)" \
		-derivedDataPath "$(DERIVED_DATA)" \
		-destination "$(CATALYST_DESTINATION)" \
		build

clean:
	cd "$(RUST_CRATE_DIR)" && cargo clean
	rm -rf "$(DERIVED_DATA)"