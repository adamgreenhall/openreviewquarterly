class Piece < ActiveRecord::Base
  attr_accessible :author_id, :issue_id, :number, :title, :type
  belongs_to :issue
  belongs_to :author
end
