class Piece < ActiveRecord::Base
  attr_accessible :author_id, :issue_id, :number, :title, :kind, :content
  validates_presence_of :title, :author_id
  belongs_to :issue
  belongs_to :author
  def is_published
    self.issue.is_published
  end
  def nice_name
    (self.title.nil? || self.title=='') ? 'Untitled' : self.title
  end
end
