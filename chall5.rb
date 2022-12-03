# This code snippets is used within a Rails web application. 
# Consider that the views code is written in safe manner and all data
# is escaped on the output

########### Controller code ###########
require "yaml"

class UserUploadsController < ApplicationController
  # includes Uploads module for #respond_to_upload method
  include Uploads


  def create
    @upload = current_user.user_uploads.new
    
    respond_to_upload(request) do |file, response|
      # grab uploaded file
      @upload.yml = file
      # try to save it
      if response[:success] = @upload.save
        # send back upload id and image preview
        response[:user_upload_id] = @upload.id
        # try to parse it
        YAML.load(File.read(@upload.path))
        # return parsed YAML data
        response[:user_upload_preview_url] = @upload.yaml.url(:yaml_editor)
      else
        # report errors if any
        response[:errors] = @upload.errors
      end
    end
  end
end

########### Part of the views code ###########

#upload-area data-button='#upload-button' \
               data-multiple='false' \
               data-dropzones='#upload-area'
    a#upload-button Choose a yaml file


########## Part of the JS code #########

  $('#upload-area').uploader
    request:
      endpoint: '/user_uploads'
    validation:
      allowedExtensions: ['yaml']
    callbacks:
      onComplete: (id, fileName, response) ->
        console.log('onComplete')
      onProgress: (id, fileName, loaded, total) ->
        console.log('onProgress')
      onUpload: (id, fileName) ->
        console.log('onUpload')
      onError: (id, fileName, message) ->
        console.log('onError')