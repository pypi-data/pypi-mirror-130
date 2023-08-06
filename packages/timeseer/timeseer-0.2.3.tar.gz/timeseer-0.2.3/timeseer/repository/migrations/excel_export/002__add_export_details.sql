-- depends: 001__create

create table Series_ExcelExport_EventFrames (
    id integer primary key autoincrement,
    series_excel_export_id int not null,
    frame_type text not null,

    foreign key (series_excel_export_id) references Series_ExcelExport(id) on delete cascade
);

alter table Series_ExcelExport add column start_date datetime;
alter table Series_ExcelExport add column end_date datetime;
